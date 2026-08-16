from scm_ontology.decision_authorization import (
    AuthorizedDecision,
    DecisionAuthorizationError,
    authorize_decision,
)
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


def test_authorize_decision_is_immutable_and_deterministic():
    result = authorize_decision(
        validated_proposal(),
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-16T22:30:00Z",
    )
    assert isinstance(result, AuthorizedDecision)
    assert result.context_id == "ctx-1"
    assert result.to_mapping() == {
        "contract_version": "S345.1",
        "context_id": "ctx-1",
        "proposal": {"action": "replenish"},
        "actor_id": "planner-1",
        "authority": "supply-chain-manager",
        "authorized_at": "2026-08-16T22:30:00Z",
        "evidence_ids": ["e1"],
        "provenance_ids": ["p1"],
    }


def test_authorize_decision_rejects_blank_actor():
    try:
        authorize_decision(
            validated_proposal(),
            actor_id=" ",
            authority="manager",
            authorized_at="2026-08-16T22:30:00Z",
        )
    except DecisionAuthorizationError:
        pass
    else:
        raise AssertionError("blank actor must be rejected")


def test_authorize_decision_rejects_blank_authority():
    try:
        authorize_decision(
            validated_proposal(),
            actor_id="planner-1",
            authority=" ",
            authorized_at="2026-08-16T22:30:00Z",
        )
    except DecisionAuthorizationError:
        pass
    else:
        raise AssertionError("blank authority must be rejected")


def test_authorize_decision_rejects_blank_timestamp():
    try:
        authorize_decision(
            validated_proposal(),
            actor_id="planner-1",
            authority="manager",
            authorized_at=" ",
        )
    except DecisionAuthorizationError:
        pass
    else:
        raise AssertionError("blank timestamp must be rejected")
