"""Immutable execution-command boundary for authorized decisions."""
from __future__ import annotations

from dataclasses import dataclass

from .decision_authorization import AuthorizedDecision


class ExecutionCommandError(ValueError):
    """Raised when an execution command cannot be constructed."""


@dataclass(frozen=True)
class ExecutionCommand:
    """Canonical command envelope; it does not execute anything."""

    decision: AuthorizedDecision
    command_type: str
    command_id: str

    def __post_init__(self) -> None:
        if not self.command_type.strip():
            raise ExecutionCommandError("command_type must be non-empty")
        if not self.command_id.strip():
            raise ExecutionCommandError("command_id must be non-empty")

    @property
    def context_id(self) -> str:
        return self.decision.context_id

    def to_mapping(self) -> dict[str, object]:
        return {
            "contract_version": "S346.1",
            "command_id": self.command_id,
            "command_type": self.command_type,
            "context_id": self.context_id,
            "proposal": self.decision.proposal.output.proposal,
            "actor_id": self.decision.actor_id,
            "authority": self.decision.authority,
            "authorized_at": self.decision.authorized_at,
            "evidence_ids": list(self.decision.proposal.output.evidence_ids),
            "provenance_ids": list(self.decision.proposal.output.provenance_ids),
        }


def build_execution_command(
    decision: AuthorizedDecision,
    *,
    command_type: str,
    command_id: str,
) -> ExecutionCommand:
    """Build an immutable command from an authorized decision only."""
    return ExecutionCommand(
        decision=decision,
        command_type=command_type,
        command_id=command_id,
    )
