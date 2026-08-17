"""Immutable execution-outcome boundary for external command execution."""
from __future__ import annotations

from dataclasses import dataclass

from .execution_command import ExecutionCommand


class ExecutionOutcomeError(ValueError):
    """Raised when an execution outcome is invalid."""


_ALLOWED_STATUSES = frozenset({"success", "failure", "partial", "rejected"})


@dataclass(frozen=True)
class ExecutionOutcome:
    """Canonical record of an external execution result; it has no side effects."""

    command: ExecutionCommand
    status: str
    executed_at: str
    external_reference: str | None = None
    detail: str | None = None

    def __post_init__(self) -> None:
        if self.status not in _ALLOWED_STATUSES:
            raise ExecutionOutcomeError("status must be one of success, failure, partial, rejected")
        if not self.executed_at.strip():
            raise ExecutionOutcomeError("executed_at must be non-empty")
        if self.external_reference is not None and not self.external_reference.strip():
            raise ExecutionOutcomeError("external_reference must be non-empty when provided")

    @property
    def command_id(self) -> str:
        return self.command.command_id

    @property
    def context_id(self) -> str:
        return self.command.context_id

    def to_mapping(self) -> dict[str, object]:
        return {
            "contract_version": "S347.1",
            "command_id": self.command_id,
            "context_id": self.context_id,
            "command_type": self.command.command_type,
            "status": self.status,
            "executed_at": self.executed_at,
            "external_reference": self.external_reference,
            "detail": self.detail,
            "evidence_ids": list(self.command.decision.proposal.output.evidence_ids),
            "provenance_ids": list(self.command.decision.proposal.output.provenance_ids),
        }


def record_execution_outcome(
    command: ExecutionCommand,
    *,
    status: str,
    executed_at: str,
    external_reference: str | None = None,
    detail: str | None = None,
) -> ExecutionOutcome:
    """Record an externally observed outcome without performing the execution."""
    return ExecutionOutcome(
        command=command,
        status=status,
        executed_at=executed_at,
        external_reference=external_reference,
        detail=detail,
    )
