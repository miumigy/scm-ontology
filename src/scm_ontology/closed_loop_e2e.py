"""P9-E — Closed-Loop SCM OS Execution E2E.

Composes the governed loop end to end:

```text
State -> Decision -> Authorization -> Execution -> Outcome
     -> Canonical Event -> Updated State
```

using the deterministic Phase 9 slices: the S348 governed decision loop, the
P9-C approval-to-execution runtime, the P9-B external execution adapter, and the
P9-D outcome-to-event canonicalization.

The operative ``ClosedLoopState`` is an explicit, derived operational snapshot
(``derived=True``). Applying an outcome updates that derived state only — it
never mutates Canonical Truth directly. Every outcome effect flows through the
governed execution/event boundary first, per AGENTS.md.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import json
from typing import Any

from .approval_to_execution_runtime import (
    ApprovalToExecutionResult,
    approve_and_execute,
)
from .decision_runtime import DecisionRuntimeResult, run_decision_loop
from .execution_runtime import DryRunExecutionResult
from .external_execution_adapter import (
    ExternalExecutionAdapter,
    InMemoryExternalSystem,
    ReferenceExternalExecutionAdapter,
)
from .graph_reasoning_projection import GraphReasoningObservation
from .outcome_to_event_canonicalization import canonicalize_execution_outcome
from .reasoning_input import ReasoningInput
from .reasoning_output import ReasoningOutput
from .reasoning_provider import ReasoningProvider


class ClosedLoopE2EError(ValueError):
    """Raised when a closed-loop E2E run violates its contract."""


@dataclass(frozen=True)
class ClosedLoopState:
    """Immutable, derived operational state snapshot (not Canonical Truth)."""

    derived: bool = True
    on_hand: int = 0
    open_purchase_orders: int = 0
    reorder_point: int = 0
    reorder_quantity: int = 0

    def __post_init__(self) -> None:
        if self.derived is not True:
            raise ClosedLoopE2EError("ClosedLoopState must remain explicitly derived")
        if any(v < 0 for v in (self.on_hand, self.open_purchase_orders, self.reorder_point, self.reorder_quantity)):
            raise ClosedLoopE2EError("state quantities must be non-negative")

    def to_mapping(self) -> dict[str, Any]:
        return {
            "derived": True,
            "on_hand": self.on_hand,
            "open_purchase_orders": self.open_purchase_orders,
            "reorder_point": self.reorder_point,
            "reorder_quantity": self.reorder_quantity,
        }


@dataclass(frozen=True)
class ReplenishmentRuleProvider:
    """Deterministic rule provider that proposes replenishment when stock is low."""

    provider_id: str = "closed-loop-replenishment-rule"

    def reason(self, reasoning_input: ReasoningInput) -> ReasoningOutput:
        observations = reasoning_input.observations
        on_hand = 0
        reorder_point = 0
        reorder_quantity = 0
        for obs in observations:
            value = obs.value
            if not isinstance(value, dict):
                continue
            on_hand = int(value.get("on_hand", on_hand))
            reorder_point = int(value.get("reorder_point", reorder_point))
            reorder_quantity = int(value.get("reorder_quantity", reorder_quantity))

        evidence_ids: list[str] = []
        provenance_ids: list[str] = []
        for obs in observations:
            evidence_ids.extend(obs.evidence_ids)
            provenance_ids.extend(obs.provenance_ids)

        if on_hand < reorder_point:
            proposal: dict[str, Any] = {
                "action": "replenish",
                "quantity": reorder_quantity,
                "service": "replenishment",
            }
            rationale = (
                f"on-hand {on_hand} below reorder point {reorder_point}; "
                f"propose replenish {reorder_quantity}"
            )
        else:
            proposal = {"action": "no_operation", "reason": "stock sufficient"}
            rationale = f"on-hand {on_hand} meets or exceeds reorder point {reorder_point}"

        return ReasoningOutput(
            context_id=reasoning_input.context_id,
            proposal=proposal,
            rationale=rationale,
            evidence_ids=tuple(evidence_ids),
            provenance_ids=tuple(provenance_ids),
            confidence=0.9,
        )


@dataclass(frozen=True)
class ClosedLoopE2EResult:
    """Immutable bundle of one full closed-loop iteration.

    ``executed`` distinguishes a real governed external execution (with an
    ``approval`` and a canonical event) from a ``no_operation`` decision (no
    side effect, no state change, and no execution event).
    """

    context_id: str
    command_id: str
    state_before: ClosedLoopState
    decision: DecisionRuntimeResult
    state_after: ClosedLoopState
    executed: bool
    approval: ApprovalToExecutionResult | None = None
    dry_run: DryRunExecutionResult | None = None
    canonical_event: Any | None = None

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P9E.1",
            "context_id": self.context_id,
            "command_id": self.command_id,
            "executed": self.executed,
            "state_before": self.state_before.to_mapping(),
            "decision": self.decision.to_mapping(),
            "approval": self.approval.to_mapping() if self.approval is not None else None,
            "canonical_event_type": (
                self.canonical_event.event_type if self.canonical_event is not None else None
            ),
            "canonical_event_verdict": (
                self.canonical_event.attributes.get("verdict")
                if self.canonical_event is not None
                else None
            ),
            "state_after": self.state_after.to_mapping(),
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def _derive_observations(state: ClosedLoopState) -> tuple[GraphReasoningObservation, ...]:
    return (
        GraphReasoningObservation(
            question_id="closed_loop.inventory_position",
            value={
                "on_hand": state.on_hand,
                "reorder_point": state.reorder_point,
                "reorder_quantity": state.reorder_quantity,
            },
            evidence_ids=("e-closed-loop-inventory",),
            provenance_ids=("p-derived-state",),
        ),
    )


def _apply_outcome(state: ClosedLoopState, approval: ApprovalToExecutionResult) -> ClosedLoopState:
    """Apply an outcome's succeeded elements to the derived state.

    Only succeeded elements affect the derived state; failed elements are
    ignored (the side effect did not complete). A partial result applies the
    succeeded portion. This remains a derived-state update, never canonical.
    """
    succeeded_quantity = state.reorder_quantity
    verdict = approval.outcome.verdict
    if verdict == "failure":
        return state
    if verdict == "partial":
        succeeded_quantity = max(0, succeeded_quantity // 2)
    return replace(
        state,
        on_hand=state.on_hand + succeeded_quantity,
        open_purchase_orders=state.open_purchase_orders + (
            succeeded_quantity if verdict in ("success", "partial") else 0
        ),
    )


def run_closed_loop_e2e(
    *,
    context_id: str,
    state: ClosedLoopState,
    actor_id: str,
    authority: str,
    authorized_at: str,
    command_id: str,
    adapter: ExternalExecutionAdapter | None = None,
    external_system: InMemoryExternalSystem | None = None,
) -> ClosedLoopE2EResult:
    """Run one deterministic closed-loop iteration state -> ... -> updated state.

    Composes: observation -> governed decision -> approval/execution -> outcome
    -> canonical event -> derived state update. None of these mutate Canonical
    Truth; the state update is an explicit derived projection.
    """
    if not context_id.strip():
        raise ClosedLoopE2EError("context_id must be non-empty")
    if not isinstance(state, ClosedLoopState):
        raise ClosedLoopE2EError("state must be a ClosedLoopState")
    if not actor_id.strip() or not authority.strip():
        raise ClosedLoopE2EError("actor_id and authority must be non-empty")

    if adapter is None:
        adapter = ReferenceExternalExecutionAdapter()
    provider: ReasoningProvider = ReplenishmentRuleProvider()
    observations = _derive_observations(state)

    command_type = "replenishment"
    decision = run_decision_loop(
        context_id=context_id,
        observations=observations,
        provider=provider,
        actor_id=actor_id,
        authority=authority,
        authorized_at=authorized_at,
        command_type=command_type,
        command_id=command_id,
    )

    proposal = decision.execution_command.decision.proposal.output.proposal
    if isinstance(proposal, dict) and proposal.get("action") == "no_operation":
        # No operation: no side effect, no execution event, no state change.
        return ClosedLoopE2EResult(
            context_id=context_id,
            command_id=command_id,
            state_before=state,
            decision=decision,
            state_after=state,
            executed=False,
        )

    approval = approve_and_execute(
        decision.execution_command,
        adapter=adapter,
        executed_at=authorized_at,
        actor_id=actor_id,
        external_system=external_system,
    )
    canonical_event = canonicalize_execution_outcome(approval)
    state_after = _apply_outcome(state, approval)

    return ClosedLoopE2EResult(
        context_id=context_id,
        command_id=command_id,
        state_before=state,
        decision=decision,
        state_after=state_after,
        executed=True,
        approval=approval,
        dry_run=approval.dry_run,
        canonical_event=canonical_event,
    )
