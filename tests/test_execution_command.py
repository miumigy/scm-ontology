from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.execution_command import (
    ExecutionCommand,
    ExecutionCommandError,
    build_execution_command,
)
from scm_ontology.decision_authorization import AuthorizedDecision
from scm_ontology.proposal_validation import ValidatedDecisionProposal
from scm_ontology.reasoning_input import ReasoningInput
from scm_ontology.reasoning_output import ReasoningOutput


def authorized_decision():
    reasoning_input = ReasoningInput(
        context_id="ctx-1",
        observations=(),
        evidence_ids=("e1",),
        provenance_ids=("p1",),
    )
    output = ReasoningOutput(
        input=reasoning_input,
        proposal="replenish",
        rationale="stock is below threshold",
        evidence_ids=("e1",),
        provenance_ids=("p1",),
        confidence=0.9,
    )
    validated = ValidatedDecisionProposal(output=output)
    return AuthorizedDecision(
        proposal=validated,
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-16T22:00:00Z",
    )


def test_execution_command_is_immutable_and_deterministic():
    result = build_execution_command(
        authorized_decision(), command_type="replenishment", command_id="cmd-1"
    )
    assert isinstance(result, ExecutionCommand)
    assert result.context_id == "ctx-1"
    assert result.to_mapping() == {
        "contract_version": "S346.1",
        "command_id": "cmd-1",
        "command_type": "replenishment",
        "context_id": "ctx-1",
        "proposal": "replenish",
        "actor_id": "planner-1",
        "authority": "supply-chain-manager",
        "authorized_at": "2026-08-16T22:00:00Z",
        "evidence_ids": ["e1"],
        "provenance_ids": ["p1"],
    }
    with pytest.raises(FrozenInstanceError):
        result.command_id = "cmd-2"


def test_execution_command_rejects_empty_identifiers():
    decision = authorized_decision()
    with pytest.raises(ExecutionCommandError):
        build_execution_command(decision, command_type="", command_id="cmd-1")
    with pytest.raises(ExecutionCommandError):
        build_execution_command(decision, command_type="replenishment", command_id="")
