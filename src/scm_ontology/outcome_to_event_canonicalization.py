"""P9-D — Outcome-to-Event Canonicalization (governed execution -> canonical event).

P9-D projects a governed execution outcome (P9-A ``ExecutionOutcomeContract``,
as produced through the P9-C approval-to-execution runtime) into a read-only
``CanonicalEvent`` that records the outcome as an auditable occurrence — without
bypassing governance.

Canonicalization fails closed unless the outcome came through the governed
path: it requires the post-execution ``ApprovalToExecutionResult`` whose command
lifecycle has reached the terminal ``executed`` state, and it embeds the
governance reference (command id, lifecycle state, actor chain) plus the
outcome's evidence and provenance into the event attributes.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from .approval_to_execution_runtime import ApprovalToExecutionResult
from .canonical_event import CanonicalEvent, CanonicalEventError
from .command_lifecycle import CommandState
from .execution_outcome_contract import ExecutionOutcomeContract


class OutcomeCanonicalizationError(ValueError):
    """Raised when a governed execution outcome cannot become a canonical event."""


def _iso_to_datetime(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise OutcomeCanonicalizationError(
            f"executed_at must be an ISO-8601 timestamp: {exc}"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise OutcomeCanonicalizationError("executed_at must be timezone-aware")
    return parsed


def canonicalize_execution_outcome(
    result: ApprovalToExecutionResult,
    *,
    event_occurred_at: str | None = None,
) -> CanonicalEvent:
    """Canonicalize a governed execution outcome into a read-only canonical event.

    Fails closed unless the outcome was produced by the governed
    approval-to-execution path whose lifecycle reached the terminal ``executed``
    state, so outcomes never become canonical events by bypassing governance.
    """
    if not isinstance(result, ApprovalToExecutionResult):
        raise OutcomeCanonicalizationError(
            "result must be an ApprovalToExecutionResult from the governed path"
        )
    if result.lifecycle.state != CommandState.EXECUTED:
        raise OutcomeCanonicalizationError(
            "canonicalization requires the command lifecycle to be at the "
            f"executed state; got {result.lifecycle.state.value}"
        )

    outcome: ExecutionOutcomeContract = result.outcome
    occurred_at = (
        _iso_to_datetime(event_occurred_at)
        if event_occurred_at is not None
        else _iso_to_datetime(outcome.recorded_at)
    )

    attributes: dict[str, Any] = {
        "contract_version": "P9D.1",
        "context_id": outcome.context_id,
        "command_type": outcome.command.command_type,
        "verdict": outcome.verdict,
        "outcome_id": outcome.outcome_id,
        "executed_at": outcome.recorded_at,
        "elements": [element.to_mapping() for element in outcome.elements],
        "governance_command_id": result.lifecycle.command_id,
        "governance_state": result.lifecycle.state.value,
        "governance_actors": [
            transition.actor_id for transition in result.lifecycle.transitions
        ],
        "evidence_ids": list(outcome.evidence_ids),
        "provenance_ids": list(outcome.provenance_ids),
    }

    try:
        return CanonicalEvent(
            event_type="execution_outcome_recorded",
            occurred_at=occurred_at,
            entity_id=outcome.command_id,
            attributes=attributes,
        )
    except CanonicalEventError as exc:
        raise OutcomeCanonicalizationError(str(exc)) from exc


def extract_outcome_canonical_lineage(event: CanonicalEvent) -> dict[str, object]:
    """Extract the evidence/provenance lineage embedded in a canonicalized event.

    This mirrors the S349 ``CanonicalEventLineage`` semantics as a read-only
    view so consumers can verify the event's provenance without mutating it.
    """
    attributes = event.attributes
    evidence = attributes.get("evidence_ids", ())
    provenance = attributes.get("provenance_ids", ())
    return {
        "event_id": event.entity_id,
        "evidence_ids": list(evidence),
        "provenance_ids": list(provenance),
    }
