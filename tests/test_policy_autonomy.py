import pytest

from scm_ontology.agent_tool import AgentProposal
from scm_ontology.policy_autonomy import (
    AutonomyInput,
    AutonomyLevel,
    AutonomyPolicy,
    AutonomyPolicyError,
    AutonomyVerdict,
    evaluate_autonomy,
)


def _proposal(agent_id="planner-agent", context_id="ctx-1"):
    return AgentProposal(
        agent_id=agent_id,
        context_id=context_id,
        action="replenish",
        payload={"quantity": 20},
        rationale="on-hand below reorder point",
        evidence_ids=("e-inv",),
        provenance_ids=("p-inv",),
        confidence=0.9,
    )


def _policy(scope="inventory"):
    return AutonomyPolicy(
        policy_id="policy-inv",
        allowed_by_scope={scope: AutonomyLevel.FULLY_AUTONOMOUS},
        max_monetary_impact=2000.0,
        max_confidence_required=0.7,
        max_risk_allowed=0.3,
    )


def test_high_confidence_low_risk_in_scope_is_fully_autonomous():
    verdict = evaluate_autonomy(
        _proposal(),
        inputs=AutonomyInput(confidence=0.9, risk=0.1, monetary_impact=100.0, scope="inventory"),
        policy=_policy(),
    )
    assert isinstance(verdict, AutonomyVerdict)
    assert verdict.autonomy == AutonomyLevel.FULLY_AUTONOMOUS
    assert verdict.proposal_id == _proposal().proposal_id
    assert verdict.verdict_id


def test_unknown_scope_is_blocked():
    verdict = evaluate_autonomy(
        _proposal(),
        inputs=AutonomyInput(confidence=0.9, risk=0.1, monetary_impact=100.0, scope="procurement"),
        policy=_policy(),
    )
    assert verdict.autonomy == AutonomyLevel.BLOCKED


def test_low_confidence_is_blocked():
    verdict = evaluate_autonomy(
        _proposal(),
        inputs=AutonomyInput(confidence=0.5, risk=0.1, monetary_impact=100.0, scope="inventory"),
        policy=_policy(),
    )
    assert verdict.autonomy == AutonomyLevel.BLOCKED


def test_high_risk_requires_human_review():
    verdict = evaluate_autonomy(
        _proposal(),
        inputs=AutonomyInput(confidence=0.9, risk=0.8, monetary_impact=100.0, scope="inventory"),
        policy=_policy(),
    )
    assert verdict.autonomy == AutonomyLevel.HUMAN_REVIEW


def test_high_monetary_impact_requires_approval():
    verdict = evaluate_autonomy(
        _proposal(),
        inputs=AutonomyInput(confidence=0.9, risk=0.1, monetary_impact=5000.0, scope="inventory"),
        policy=_policy(),
    )
    assert verdict.autonomy == AutonomyLevel.APPROVED


def test_scope_limited_to_approved_level():
    policy = AutonomyPolicy(
        policy_id="auto-inv",
        allowed_by_scope={"inventory": AutonomyLevel.APPROVED},
    )
    verdict = evaluate_autonomy(
        _proposal(),
        inputs=AutonomyInput(confidence=0.9, risk=0.1, monetary_impact=100.0, scope="inventory"),
        policy=policy,
    )
    assert verdict.autonomy == AutonomyLevel.APPROVED


def test_verdict_is_deterministic():
    kw = dict(
        proposal=_proposal(),
        inputs=AutonomyInput(confidence=0.9, risk=0.1, monetary_impact=100.0, scope="inventory"),
        policy=_policy(),
    )
    a = evaluate_autonomy(**kw)
    b = evaluate_autonomy(**kw)
    assert a.to_json() == b.to_json()
    assert a.verdict_id == b.verdict_id
