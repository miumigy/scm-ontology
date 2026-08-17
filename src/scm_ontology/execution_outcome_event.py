"""S348 boundary from observed execution outcomes to canonical events."""
from __future__ import annotations

from datetime import datetime

from .canonical_event import CanonicalEvent, CanonicalEventError
from .execution_outcome import ExecutionOutcome


class ExecutionOutcomeEventError(ValueError):
    """Raised when an execution outcome cannot become a canonical event."""


def execution_outcome_to_event(outcome: ExecutionOutcome) -> CanonicalEvent:
    """Project an observed execution outcome into a read-only canonical event."""
    try:
        occurred_at = datetime.fromisoformat(outcome.executed_at.replace("Z", "+00:00"))
        return CanonicalEvent(
            event_type="execution_outcome_recorded",
            occurred_at=occurred_at,
            entity_id=outcome.command_id,
            attributes={
                "contract_version": "S348.1",
                "context_id": outcome.context_id,
                "command_type": outcome.command.command_type,
                "status": outcome.status,
                "external_reference": outcome.external_reference,
                "detail": outcome.detail,
                "evidence_ids": list(outcome.command.decision.proposal.output.evidence_ids),
                "provenance_ids": list(outcome.command.decision.proposal.output.provenance_ids),
            },
        )
    except (ValueError, CanonicalEventError) as exc:
        raise ExecutionOutcomeEventError(str(exc)) from exc
