from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.execution_command import build_execution_command
from scm_ontology.execution_outcome import (
    ExecutionOutcome,
    ExecutionOutcomeError,
    record_execution_outcome,
)
from scm_ontology.decision_authorization import AuthorizedDecision
from scm_ontology.proposal_validation import ValidatedDecisionProposal
from scm_ontology.reasoning_output import ReasoningOutput


def command():
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
    return build_execution_command(decision, command_type="replenishment", command_id="cmd-1")


def test_execution_outcome_is_immutable_and_deterministic():
    result = record_execution_outcome(
        command(), status="success", executed_at="2026-08-16T22:10:00Z", external_reference="ERP-7"
    )
    assert isinstance(result, ExecutionOutcome)
    assert result.command_id == "cmd-1"
    assert result.context_id == "ctx-1"
    assert result.to_mapping() == {
        "contract_version": "S347.1",
        "command_id": "cmd-1",
        "context_id": "ctx-1",
        "command_type": "replenishment",
        "status": "success",
        "executed_at": "2026-08-16T22:10:00Z",
        "external_reference": "ERP-7",
        "detail": None,
        "evidence_ids": ["e1"],
        "provenance_ids": ["p1"],
    }
    with pytest.raises(FrozenInstanceError):
        result.status = "failure"


def test_execution_outcome_rejects_invalid_status_and_blank_timestamp():
    with pytest.raises(ExecutionOutcomeError):
        record_execution_outcome(command(), status="unknown", executed_at="2026-08-16T22:10:00Z")
    with pytest.raises(ExecutionOutcomeError):
        record_execution_outcome(command(), status="success", executed_at=" ")
    with pytest.raises(ExecutionOutcomeError):
        record_execution_outcome(
            command(), status="success", executed_at="2026-08-16T22:10:00Z", external_reference=" "
        )
