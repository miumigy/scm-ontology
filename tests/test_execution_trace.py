from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from scm_ontology.canonical_event import CanonicalEvent
from scm_ontology.canonical_event_lineage import extract_event_lineage
from scm_ontology.decision_authorization import AuthorizedDecision
from scm_ontology.execution_command import build_execution_command
from scm_ontology.execution_outcome import record_execution_outcome
from scm_ontology.execution_outcome_event import execution_outcome_to_event
from scm_ontology.execution_trace import ExecutionTrace, ExecutionTraceError, build_execution_trace
from scm_ontology.proposal_validation import ValidatedDecisionProposal
from scm_ontology.reasoning_output import ReasoningOutput


def chain():
    output = ReasoningOutput(
        context_id="ctx-1",
        proposal="replenish",
        rationale="stock is below threshold",
        evidence_ids=("e1", "e2"),
        provenance_ids=("p1", "p2"),
        confidence=0.9,
    )
    decision = AuthorizedDecision(
        proposal=ValidatedDecisionProposal(output=output),
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-16T22:00:00Z",
    )
    command = build_execution_command(decision, command_type="replenishment", command_id="cmd-1")
    outcome = record_execution_outcome(
        command, status="success", executed_at="2026-08-16T22:10:00Z", external_reference="ERP-7"
    )
    event = execution_outcome_to_event(outcome)
    lineage = extract_event_lineage(event)
    return command, outcome, event, lineage


def test_execution_trace_is_immutable_and_deterministic():
    result = build_execution_trace(*chain())
    assert isinstance(result, ExecutionTrace)
    assert result.to_mapping() == {
        "contract_version": "S350.1",
        "context_id": "ctx-1",
        "proposal": "replenish",
        "actor_id": "planner-1",
        "authority": "supply-chain-manager",
        "command_id": "cmd-1",
        "command_type": "replenishment",
        "outcome_status": "success",
        "event_id": "cmd-1",
        "event_type": "execution_outcome_recorded",
        "evidence_ids": ["e1", "e2"],
        "provenance_ids": ["p1", "p2"],
    }
    with pytest.raises(FrozenInstanceError):
        result.command_id = "cmd-2"


def test_trace_rejects_cross_context_or_lineage_mismatch():
    command, outcome, event, lineage = chain()
    bad_outcome = type(outcome)(
        command=build_execution_command(
            AuthorizedDecision(
                proposal=ValidatedDecisionProposal(
                    output=ReasoningOutput(
                        context_id="ctx-2", proposal="replenish", rationale="other", evidence_ids=("e1",), provenance_ids=("p1",)
                    )
                ),
                actor_id="planner-1", authority="supply-chain-manager", authorized_at="2026-08-16T22:00:00Z",
            ),
            command_type="replenishment", command_id="cmd-2",
        ),
        status="success", executed_at="2026-08-16T22:10:00Z",
    )
    with pytest.raises(ExecutionTraceError, match="command_id"):
        build_execution_trace(command, bad_outcome, event, lineage)


def test_trace_rejects_wrong_event_type():
    command, outcome, _, lineage = chain()
    bad_event = CanonicalEvent(
        event_type="other_event",
        occurred_at=datetime(2026, 8, 16, 22, 10, tzinfo=timezone.utc),
        entity_id="cmd-1",
        attributes={"context_id": "ctx-1"},
    )
    with pytest.raises(ExecutionTraceError, match="event_type"):
        build_execution_trace(command, outcome, bad_event, lineage)
