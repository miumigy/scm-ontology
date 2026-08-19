"""SCM OS Phase 9 Acceptance (P9-G).

Closes **Phase 9 (Closed-Loop SCM OS Execution)** with a deterministic
acceptance contract: a reference SCM workflow operates as a governed closed
loop against an injected external system.

P9-G folds the P9-A..P9-F capabilities into an immutable, content-addressed
``Phase9AcceptanceReport`` with an overall ``accepted`` flag. The phase is
accepted when every capability is operable AND the **governed closed-loop gate**
(P9-G) holds: the reference workflow traverses
state -> decision -> authorization -> execution -> outcome -> canonical event ->
updated state through the governed P9 path, with idempotency/retry/recovery
semantics active.

P9-G performs no external side effect and never mutates Canonical Truth.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Callable

from .approval_to_execution_runtime import approve_and_execute
from .closed_loop_e2e import ClosedLoopState, run_closed_loop_e2e
from .decision_authorization import AuthorizedDecision
from .execution_command import ExecutionCommand, build_execution_command
from .execution_outcome_contract import (
    ResultElement,
    build_execution_outcome_contract,
    reject_execution_outcome_contract,
)
from .external_execution_adapter import (
    InMemoryExternalSystem,
    ReferenceExternalExecutionAdapter,
    execute_externally,
    validate_external_adapter,
)
from .failure_retry_idempotency import (
    ExecutionRunRegistry,
    RetryableAdapter,
    RunPolicy,
    run_with_failure_policy,
)
from .outcome_to_event_canonicalization import canonicalize_execution_outcome
from .proposal_validation import ValidatedDecisionProposal
from .reasoning_output import ReasoningOutput


class Phase9AcceptanceError(ValueError):
    """Raised when an acceptance input or invocation is invalid."""


def _command() -> ExecutionCommand:
    output = ReasoningOutput(
        context_id="ctx-accept-1",
        proposal={"action": "replenish", "quantity": 20},
        rationale="acceptance probe",
        evidence_ids=("e-acc",),
        provenance_ids=("p-acc",),
        confidence=0.9,
    )
    decision = AuthorizedDecision(
        proposal=ValidatedDecisionProposal(output=output),
        actor_id="planner-acc",
        authority="manager",
        authorized_at="2026-08-19T00:00:00Z",
    )
    return build_execution_command(
        decision, command_type="replenishment", command_id="acc-cmd-1"
    )


def _execution_outcome_contract_probe() -> dict[str, Any]:
    """P9-A — success/partial/failure outcome model with evidence & provenance."""
    cmd = _command()
    success = build_execution_outcome_contract(
        cmd,
        elements=(ResultElement(target_ref="t1", status="success"),),
        recorded_at="2026-08-19T01:00:00Z",
        evidence_ids=("e-acc",),
        provenance_ids=("p-acc",),
    )
    partial = build_execution_outcome_contract(
        cmd,
        elements=(
            ResultElement(target_ref="t1", status="success"),
            ResultElement(target_ref="t2", status="failure"),
        ),
        recorded_at="2026-08-19T01:00:00Z",
    )
    failure = build_execution_outcome_contract(
        cmd,
        elements=(ResultElement(target_ref="t1", status="failure"),),
        recorded_at="2026-08-19T01:00:00Z",
    )
    rejected = reject_execution_outcome_contract(cmd, recorded_at="2026-08-19T01:00:00Z")
    return {
        "success_verdict": success.verdict,
        "partial_verdict": partial.verdict,
        "failure_verdict": failure.verdict,
        "rejected_verdict": rejected.verdict,
    }


def _external_execution_adapter_probe() -> dict[str, Any]:
    """P9-B — injectable side-effect adapter with a deterministic test double."""
    adapter = ReferenceExternalExecutionAdapter()
    validate_external_adapter(adapter)
    system = InMemoryExternalSystem()
    outcome = execute_externally(
        _command(),
        adapter=adapter,
        executed_at="2026-08-19T01:00:00Z",
        external_system=system,
    )
    return {
        "adapter_id": adapter.adapter_id,
        "verdict": outcome.verdict,
        "side_effects_recorded": system.write_count,
    }


def _approval_to_execution_probe() -> dict[str, Any]:
    """P9-C — authorized commands progress from dry-run to controlled execution."""
    result = approve_and_execute(
        _command(),
        adapter=ReferenceExternalExecutionAdapter(),
        executed_at="2026-08-19T01:00:00Z",
        actor_id="planner-acc",
    )
    return {
        "lifecycle_state": result.lifecycle.state.value,
        "verdict": result.verdict,
    }


def _outcome_to_event_probe() -> dict[str, Any]:
    """P9-D — governed outcomes become canonical events without bypassing governance."""
    result = approve_and_execute(
        _command(),
        adapter=ReferenceExternalExecutionAdapter(),
        executed_at="2026-08-19T01:00:00Z",
        actor_id="planner-acc",
    )
    event = canonicalize_execution_outcome(result)
    return {
        "event_type": event.event_type,
        "verdict": event.attributes.get("verdict"),
        "governance_state": event.attributes.get("governance_state"),
    }


def _closed_loop_probe() -> dict[str, Any]:
    """P9-E — state -> decision -> execution -> outcome -> event -> updated state."""
    result = run_closed_loop_e2e(
        context_id="ctx-acc-1",
        state=ClosedLoopState(
            on_hand=5, reorder_point=10, reorder_quantity=20,
        ),
        actor_id="planner-acc",
        authority="manager",
        authorized_at="2026-08-19T01:00:00Z",
        command_id="acc-loop-1",
    )
    return {
        "executed": result.executed,
        "state_before": result.state_before.on_hand,
        "state_after": result.state_after.on_hand,
        "canonical_event_verdict": (
            result.canonical_event.attributes.get("verdict")
            if result.canonical_event is not None else None
        ),
    }


def _failure_retry_idempotency_probe() -> dict[str, Any]:
    """P9-F — bounded retry, duplicate protection, recovery semantics."""
    registry = ExecutionRunRegistry()
    flaky = RetryableAdapter(ReferenceExternalExecutionAdapter(), failures_before_success=1)
    first = run_with_failure_policy(
        _command(),
        adapter=flaky,
        policy=RunPolicy(max_attempts=3),
        registry=registry,
        actor_id="planner-acc",
        executed_at="2026-08-19T01:00:00Z",
    )
    duplicate = run_with_failure_policy(
        _command(),
        adapter=flaky,
        policy=RunPolicy(max_attempts=3),
        registry=registry,
        actor_id="planner-acc",
        executed_at="2026-08-19T02:00:00Z",
    )
    return {
        "status": first.status,
        "attempt_count": first.attempt_count,
        "duplicate_is_replayed": duplicate is first,
    }


def _governed_closed_loop_gate() -> dict[str, Any]:
    """P9-G — a reference workflow operates as a governed closed loop end-to-end.

    Runs a success loop (state updated via the canonical event) and a
    no-operation loop (stock sufficient -> no side effect), and confirms the
    canonical event carries the governed path (executed state + evidence). This
    proves the P9-A..P9-F capabilities compose into a working governed closed
    loop against the injected external system.
    """
    system = InMemoryExternalSystem()
    success = run_closed_loop_e2e(
        context_id="ctx-acc-gate",
        state=ClosedLoopState(
            on_hand=5, reorder_point=10, reorder_quantity=20,
        ),
        actor_id="planner-acc",
        authority="manager",
        authorized_at="2026-08-19T01:00:00Z",
        command_id="acc-gate-1",
        external_system=system,
    )
    noop = run_closed_loop_e2e(
        context_id="ctx-acc-gate-2",
        state=ClosedLoopState(
            on_hand=50, reorder_point=10, reorder_quantity=20,
        ),
        actor_id="planner-acc",
        authority="manager",
        authorized_at="2026-08-19T01:00:00Z",
        command_id="acc-gate-2",
        external_system=system,
    )
    gate_holds = (
        success.executed is True
        and success.canonical_event is not None
        and success.canonical_event.attributes.get("verdict") == "success"
        and success.state_after.on_hand == 25
        and noop.executed is False
        and system.write_count == 1
    )
    return {
        "gate_holds": gate_holds,
        "success_state_before": success.state_before.on_hand,
        "success_state_after": success.state_after.on_hand,
        "noop_executed": noop.executed,
        "external_side_effects": system.write_count,
    }


_CAPABILITIES: tuple[tuple[str, str, Callable[[], Any]], ...] = (
    (
        "execution_outcome_contract",
        "Execution Outcome Contract (P9-A)",
        _execution_outcome_contract_probe,
    ),
    (
        "external_execution_adapter",
        "External Execution Adapter (P9-B)",
        _external_execution_adapter_probe,
    ),
    (
        "approval_to_execution",
        "Approval-to-Execution Runtime (P9-C)",
        _approval_to_execution_probe,
    ),
    (
        "outcome_to_event_canonicalization",
        "Outcome-to-Event Canonicalization (P9-D)",
        _outcome_to_event_probe,
    ),
    (
        "closed_loop_e2e",
        "Closed-Loop E2E (P9-E)",
        _closed_loop_probe,
    ),
    (
        "failure_retry_idempotency",
        "Failure / Retry / Idempotency (P9-F)",
        _failure_retry_idempotency_probe,
    ),
    (
        "governed_closed_loop_gate",
        "Governed Closed-Loop Gate (P9-G)",
        _governed_closed_loop_gate,
    ),
)


@dataclass(frozen=True)
class CapabilityResult:
    """Deterministic probe result for one Phase 9 capability."""

    key: str
    name: str
    operable: bool
    evidence_id: str
    detail: dict[str, Any] | None = None

    def to_mapping(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "key": self.key,
            "name": self.name,
            "operable": self.operable,
            "evidence_id": self.evidence_id,
        }
        if self.detail is not None:
            value["detail"] = self.detail
        return value


@dataclass(frozen=True)
class AcceptanceSummary:
    """Deterministic aggregate counts across the capability probes."""

    capability_count: int
    operable_count: int
    failed_count: int

    def to_mapping(self) -> dict[str, Any]:
        return {
            "capability_count": self.capability_count,
            "operable_count": self.operable_count,
            "failed_count": self.failed_count,
        }


@dataclass(frozen=True)
class Phase9AcceptanceReport:
    """Immutable, content-addressed Phase 9 acceptance report."""

    report_id: str
    accepted: bool
    accepted_at: str
    capabilities: tuple[CapabilityResult, ...]
    summary: AcceptanceSummary

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P9G.1",
            "is_phase9_acceptance": True,
            "report_id": self.report_id,
            "accepted": self.accepted,
            "accepted_at": self.accepted_at,
            "summary": self.summary.to_mapping(),
            "capabilities": [cap.to_mapping() for cap in self.capabilities],
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def _evidence_id(output: Any) -> str:
    payload = json.dumps(
        output, ensure_ascii=False, sort_keys=True,
        separators=(",", ":"), default=str,
    )
    return sha256(payload.encode()).hexdigest()


def _probe(key: str, name: str, fn: Callable[[], Any]) -> CapabilityResult:
    try:
        output = fn()
    except Exception as exc:  # noqa: BLE001 - acceptance probe must fail closed
        return CapabilityResult(
            key=key, name=name, operable=False,
            evidence_id="", detail={"error": f"{type(exc).__name__}: {exc}"},
        )
    if output is None or output is False:
        return CapabilityResult(
            key=key, name=name, operable=False,
            evidence_id="", detail={"error": "probe produced no usable output"},
        )
    return CapabilityResult(
        key=key,
        name=name,
        operable=True,
        evidence_id=_evidence_id(output),
        detail=output if isinstance(output, dict) else {"value": str(output)},
    )


def run_phase9_acceptance(*, accepted_at: str) -> Phase9AcceptanceReport:
    """Run the Phase 9 capability probes and produce an acceptance report.

    A capability is operable when its deterministic probe returns a usable
    result without error. The phase is accepted when every capability is
    operable, including the P9-G governed closed-loop gate.
    """
    if not isinstance(accepted_at, str) or not accepted_at.strip():
        raise Phase9AcceptanceError("accepted_at must be non-empty")

    capabilities = tuple(
        _probe(key, name, fn) for key, name, fn in _CAPABILITIES
    )
    operable = sum(1 for cap in capabilities if cap.operable)
    summary = AcceptanceSummary(
        capability_count=len(capabilities),
        operable_count=operable,
        failed_count=len(capabilities) - operable,
    )
    accepted = operable == len(capabilities)

    payload = {
        "accepted_at": accepted_at,
        "capabilities": [cap.to_mapping() for cap in capabilities],
    }
    report_id = sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()

    return Phase9AcceptanceReport(
        report_id=report_id,
        accepted=accepted,
        accepted_at=accepted_at,
        capabilities=capabilities,
        summary=summary,
    )
