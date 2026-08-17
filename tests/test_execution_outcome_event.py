from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.decision_authorization import AuthorizedDecision
from scm_ontology.execution_command import build_execution_command
from scm_ontology.execution_outcome import record_execution_outcome
from scm_ontology.execution_outcome_event import (
    ExecutionOutcomeEventError,
    execution_outcome_to_event,
)
from scm_ontology.proposal_validation import ValidatedDecisionProposal
from scm_ontology.reasoning_output import ReasoningOutput


def outcome():
    output = ReasoningOutput(
        context_id="ctx-1",
        proposal="replenish",
        rationale="stock is below threshold",
        evidence_ids=("e1",),
        provenance_ids=("p1",),
        confidence=0.9,
    )
    decision = AuthorizedDecision(
        proposal=ValidatedDecisionProposal(output=output),
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-16T22:00:00Z",
    )
    command = build_execution_command(
        decision, command_type="replenishment", command_id="cmd-1"
    )
    return record_execution_outcome(
        command,
        status="success",
        executed_at="2026-08-16T22:10:00Z",
        external_reference="ERP-7",
    )


def test_execution_outcome_maps_to_deterministic_canonical_event():
    event = execution_outcome_to_event(outcome())
    assert event.event_type == "execution_outcome_recorded"
    assert event.entity_id == "cmd-1"
    assert event.occurred_at.isoformat() == "2026-08-16T22:10:00+00:00"
    assert dict(event.attributes) == {
        "contract_version": "S348.1",
        "context_id": "ctx-1",
        "command_type": "replenishment",
        "status": "success",
        "external_reference": "ERP-7",
        "detail": None,
        "evidence_ids": ["e1"],
        "provenance_ids": ["p1"],
    }


def test_projection_does_not_mutate_outcome():
    result = outcome()
    event = execution_outcome_to_event(result)
    assert result.status == "success"
    with pytest.raises(FrozenInstanceError):
        result.status = "failure"
    assert event.entity_id == result.command_id


def test_projection_rejects_invalid_timestamp():
    result = outcome()
    invalid = type(result)(
        command=result.command,
        status=result.status,
        executed_at="not-a-timestamp",
        external_reference=result.external_reference,
        detail=result.detail,
    )
    with pytest.raises(ExecutionOutcomeEventError):
        execution_outcome_to_event(invalid)
