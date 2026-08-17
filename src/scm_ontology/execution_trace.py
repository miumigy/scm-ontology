"""Immutable traceability across governed reasoning and execution stages."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical_event import CanonicalEvent
from .canonical_event_lineage import CanonicalEventLineage
from .execution_command import ExecutionCommand
from .execution_outcome import ExecutionOutcome


class ExecutionTraceError(ValueError):
    """Raised when the governed execution trace is inconsistent."""


@dataclass(frozen=True)
class ExecutionTrace:
    """Read-only trace linking one governed decision chain to its observed event."""

    context_id: str
    proposal: Any
    actor_id: str
    authority: str
    command_id: str
    command_type: str
    outcome_status: str
    event_id: str
    event_type: str
    evidence_ids: tuple[str, ...]
    provenance_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in ("context_id", "actor_id", "authority", "command_id", "command_type", "event_id", "event_type"):
            if not getattr(self, name).strip():
                raise ExecutionTraceError(f"{name} must be non-empty")
        if not self.evidence_ids:
            raise ExecutionTraceError("evidence_ids must be non-empty")
        if not self.provenance_ids:
            raise ExecutionTraceError("provenance_ids must be non-empty")

    def to_mapping(self) -> dict[str, object]:
        return {
            "contract_version": "S350.1",
            "context_id": self.context_id,
            "proposal": self.proposal,
            "actor_id": self.actor_id,
            "authority": self.authority,
            "command_id": self.command_id,
            "command_type": self.command_type,
            "outcome_status": self.outcome_status,
            "event_id": self.event_id,
            "event_type": self.event_type,
            "evidence_ids": list(self.evidence_ids),
            "provenance_ids": list(self.provenance_ids),
        }


def build_execution_trace(
    command: ExecutionCommand,
    outcome: ExecutionOutcome,
    event: CanonicalEvent,
    lineage: CanonicalEventLineage,
) -> ExecutionTrace:
    """Assemble and validate a deterministic read-only trace from existing contracts."""
    output = command.decision.proposal.output
    if outcome.command_id != command.command_id:
        raise ExecutionTraceError("outcome command_id must match command")
    if outcome.context_id != command.context_id:
        raise ExecutionTraceError("outcome context_id must match command")
    if event.entity_id != command.command_id:
        raise ExecutionTraceError("event entity_id must match command_id")
    if event.attributes.get("context_id") != command.context_id:
        raise ExecutionTraceError("event context_id must match command context")
    if lineage.event_id != event.entity_id:
        raise ExecutionTraceError("lineage event_id must match event")
    if lineage.evidence_ids != tuple(output.evidence_ids):
        raise ExecutionTraceError("lineage evidence_ids must match decision evidence")
    if lineage.provenance_ids != tuple(output.provenance_ids):
        raise ExecutionTraceError("lineage provenance_ids must match decision provenance")
    if event.event_type != "execution_outcome_recorded":
        raise ExecutionTraceError("event_type must be execution_outcome_recorded")
    return ExecutionTrace(
        context_id=command.context_id,
        proposal=output.proposal,
        actor_id=command.decision.actor_id,
        authority=command.decision.authority,
        command_id=command.command_id,
        command_type=command.command_type,
        outcome_status=outcome.status,
        event_id=event.entity_id,
        event_type=event.event_type,
        evidence_ids=tuple(lineage.evidence_ids),
        provenance_ids=tuple(lineage.provenance_ids),
    )
