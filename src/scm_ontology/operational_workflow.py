"""SCM Operational Workflow Application (Phase 5, S366).

Consumes the governed decision output produced by the R5/Phase 5 applications
(replenishment S358, procurement S360, production S361, distribution S362) and
turns it into an operational workflow: each governed decision is audited,
tracked through its command lifecycle, and folded into a deterministic
workflow report.

S366 does not re-derive any decision. It reuses the S348 governed loop output
(GovernedExecutionResult), the S354 governed-audit boundary, and the S355
command-lifecycle state machine. It introduces no new canonical semantics and
performs no external side effect.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any

from .command_lifecycle import (
    CommandLifecycle,
    CommandState,
    start_command_lifecycle,
    transition_command,
)
from .distribution_application import DistributionDecision
from .execution_runtime import GovernedExecutionResult
from .governed_audit import (
    GovernedDecisionAuditEntry,
    record_governed_decision,
)
from .procurement_application import ProcurementDecision
from .production_application import ProductionDecision
from .replenishment_application import ReplenishmentDecision


class OperationalWorkflowError(ValueError):
    """Raised when an operational workflow input or invocation is invalid."""


# Supported R5 decision types keyed by their application name.
_DECISION_TYPES: dict[str, type] = {
    "replenishment": ReplenishmentDecision,
    "procurement": ProcurementDecision,
    "production": ProductionDecision,
    "distribution": DistributionDecision,
}


@dataclass(frozen=True)
class OperationalStep:
    """One governed decision bound to its workflow step."""

    step_id: str
    application: str
    command_id: str
    decision: Any

    def __post_init__(self) -> None:
        if not isinstance(self.step_id, str) or not self.step_id.strip():
            raise OperationalWorkflowError("step_id must be non-empty")
        if self.application not in _DECISION_TYPES:
            raise OperationalWorkflowError(
                f"unsupported application: {self.application}"
            )
        if not isinstance(self.command_id, str) or not self.command_id.strip():
            raise OperationalWorkflowError("command_id must be non-empty")
        expected = _DECISION_TYPES[self.application]
        if not isinstance(self.decision, expected):
            raise OperationalWorkflowError(
                f"step {self.step_id!r}: decision must be a {expected.__name__}"
            )


@dataclass(frozen=True)
class WorkflowStepResult:
    """Immutable outcome of one operational workflow step."""

    step_id: str
    application: str
    state: str
    command_id: str
    audit_id: str | None = None

    def to_mapping(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "step_id": self.step_id,
            "application": self.application,
            "state": self.state,
            "command_id": self.command_id if self.command_id else None,
        }
        if self.audit_id is not None:
            value["audit_id"] = self.audit_id
        return value


@dataclass(frozen=True)
class OperationalWorkflowResult:
    """Immutable bundle of every governed step plus a workflow summary."""

    workflow_id: str
    steps: tuple[WorkflowStepResult, ...]

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "S366.1",
            "workflow_id": self.workflow_id,
            "step_count": len(self.steps),
            "actionable_steps": sum(1 for s in self.steps if s.audit_id is not None),
            "no_action_steps": sum(1 for s in self.steps if s.audit_id is None),
            "steps": [s.to_mapping() for s in self.steps],
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def _process_governed_step(
    governed: GovernedExecutionResult,
    command_id: str,
    recorded_at: str,
    actor_id: str,
) -> tuple[GovernedDecisionAuditEntry, CommandLifecycle]:
    """Audit a governed decision and advance its command to the dry-run state."""
    entry = record_governed_decision(
        governed.decision,
        recorded_at=recorded_at,
        dry_run=governed.dry_run,
    )
    lifecycle = start_command_lifecycle(command_id)
    lifecycle = transition_command(
        lifecycle, to_state=CommandState.AUTHORIZED,
        occurred_at=recorded_at, actor_id=actor_id, reason="authorize in workflow",
    )
    lifecycle = transition_command(
        lifecycle, to_state=CommandState.APPROVED,
        occurred_at=recorded_at, actor_id=actor_id, reason="approve in workflow",
    )
    lifecycle = transition_command(
        lifecycle, to_state=CommandState.DRY_RUN,
        occurred_at=recorded_at, actor_id=actor_id, reason="dry run in workflow",
    )
    return entry, lifecycle


def run_operational_workflow(
    steps: Any,
    *,
    workflow_id: str,
    recorded_at: str,
    actor_id: str,
) -> OperationalWorkflowResult:
    """Run a governed decision set through the operational workflow.

    Each step with a governed result is audited (S354) and advanced to the
    dry-run state of its command lifecycle (S355). A ``no_action`` step (no
    governed result) is recorded as ``no_action`` with no audit id.
    """
    if not isinstance(workflow_id, str) or not workflow_id.strip():
        raise OperationalWorkflowError("workflow_id must be non-empty")
    if not isinstance(recorded_at, str) or not recorded_at.strip():
        raise OperationalWorkflowError("recorded_at must be non-empty")
    if not isinstance(actor_id, str) or not actor_id.strip():
        raise OperationalWorkflowError("actor_id must be non-empty")

    try:
        steps_tuple = tuple(steps)
    except TypeError as exc:
        raise OperationalWorkflowError("steps must be iterable") from exc
    if not steps_tuple:
        raise OperationalWorkflowError("steps must not be empty")

    step_ids = [s.step_id for s in steps_tuple]
    if len(step_ids) != len(set(step_ids)):
        raise OperationalWorkflowError("step ids must be unique within the workflow")

    results: list[WorkflowStepResult] = []
    for step in steps_tuple:
        governed = getattr(step.decision, "governed", None)
        if governed is None:
            results.append(
                WorkflowStepResult(
                    step_id=step.step_id,
                    application=step.application,
                    state="no_action",
                    command_id=step.command_id,
                    audit_id=None,
                )
            )
            continue

        entry, _lifecycle = _process_governed_step(
            governed,
            command_id=step.command_id,
            recorded_at=recorded_at,
            actor_id=actor_id,
        )
        results.append(
            WorkflowStepResult(
                step_id=step.step_id,
                application=step.application,
                state="dry_run",
                command_id=step.command_id,
                audit_id=entry.audit_id,
            )
        )

    return OperationalWorkflowResult(workflow_id=workflow_id, steps=tuple(results))
