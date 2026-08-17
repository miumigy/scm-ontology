import pytest

from scm_ontology.decision_authorization import DecisionAuthorizationError, authorize_decision
from scm_ontology.proposal_validation import ValidatedDecisionProposal
from scm_ontology.reasoning_output import ReasoningOutput


def validated_proposal():
    return ValidatedDecisionProposal(
        output=ReasoningOutput(
            context_id="ctx-1",
            proposal={"action": "replenish"},
            rationale="supported by evidence",
            evidence_ids=("e1",),
            provenance_ids=("p1",),
            confidence=0.9,
        )
    )


def test_s369_authorization_is_immutable_and_metadata_preserving():
    result = authorize_decision(
        validated_proposal(),
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-17T12:00:00Z",
    )
    assert result.context_id == "ctx-1"
    assert result.to_mapping() == {
        "contract_version": "S345.1",
        "context_id": "ctx-1",
        "proposal": {"action": "replenish"},
        "actor_id": "planner-1",
        "authority": "supply-chain-manager",
        "authorized_at": "2026-08-17T12:00:00Z",
        "evidence_ids": ["e1"],
        "provenance_ids": ["p1"],
    }


def test_s369_authorization_rejects_blank_governance_metadata():
    proposal = validated_proposal()
    with pytest.raises(DecisionAuthorizationError):
        authorize_decision(proposal, actor_id=" ", authority="manager", authorized_at="t")
    with pytest.raises(DecisionAuthorizationError):
        authorize_decision(proposal, actor_id="planner-1", authority=" ", authorized_at="t")
    with pytest.raises(DecisionAuthorizationError):
        authorize_decision(proposal, actor_id="planner-1", authority="manager", authorized_at=" ")
