import pytest

from scm_ontology.agent_tool import AgentProposal
from scm_ontology.authorization_governance import ApprovalRecord, DecisionOverride
from scm_ontology.human_control import (
    ControlPath,
    HumanControlError,
    HumanControlRecord,
    HumanReviewDecision,
    route_human_control,
)
from scm_ontology.policy_autonomy import AutonomyLevel, AutonomyPolicy, AutonomyVerdict, evaluate_autonomy


def _proposal():
    return AgentProposal(
        agent_id="planner-agent",
        context_id="ctx-1",
        action="replenish",
        payload={"quantity": 20},
        rationale="on-hand below reorder point",
        evidence_ids=("e-inv",),
        provenance_ids=("p-inv",),
        confidence=0.9,
    )


def _verdict(level: AutonomyLevel) -> AutonomyVerdict:
    proposal = _proposal()
    policy = AutonomyPolicy(
        policy_id="p-inv",
        allowed_by_scope={"inventory": level},
        max_monetary_impact=2000.0,
        max_confidence_required=0.7,
        max_risk_allowed=0.3,
    )
    from scm_ontology.policy_autonomy import AutonomyInput
    return evaluate_autonomy(
        proposal,
        inputs=AutonomyInput(confidence=0.9, risk=0.1, monetary_impact=100.0, scope="inventory"),
        policy=policy,
    )


def test_fully_autonomous_records_autonomous_path():
    record = route_human_control(
        _proposal(),
        verdict=_verdict(AutonomyLevel.FULLY_AUTONOMOUS),
        at="2026-08-19T01:00:00Z",
    )
    assert isinstance(record, HumanControlRecord)
    assert record.path is ControlPath.AUTONOMOUS
    assert record.record_id


def test_approved_requires_explicit_human_approval():
    record = route_human_control(
        _proposal(),
        verdict=_verdict(AutonomyLevel.APPROVED),
        review_decision=HumanReviewDecision(decision="approve", ruled_by="manager", at="2026-08-19T01:00:00Z", reason="ok"),
        reviewer_id="manager",
        at="2026-08-19T01:00:00Z",
    )
    assert record.path is ControlPath.APPROVAL
    assert record.approval is not None
    assert isinstance(record.approval, ApprovalRecord)
    assert record.approval.approver_id == "manager"


def test_approved_without_approval_rejected():
    record = route_human_control(
        _proposal(),
        verdict=_verdict(AutonomyLevel.APPROVED),
        at="2026-08-19T01:00:00Z",
    )
    assert record.path is ControlPath.REJECTED


def test_human_review_escalates():
    record = route_human_control(
        _proposal(),
        verdict=_verdict(AutonomyLevel.HUMAN_REVIEW),
        at="2026-08-19T01:00:00Z",
    )
    assert record.path is ControlPath.ESCALATION


def test_human_review_senior_override():
    record = route_human_control(
        _proposal(),
        verdict=_verdict(AutonomyLevel.HUMAN_REVIEW),
        review_decision=HumanReviewDecision(decision="override", ruled_by="senior", at="2026-08-19T01:00:00Z", reason="justified"),
        reviewer_id="sr-planner",
        senior_id="vice-president",
        at="2026-08-19T01:00:00Z",
    )
    assert record.path is ControlPath.OVERRIDE
    assert record.override is not None
    assert isinstance(record.override, DecisionOverride)
    assert record.override.actor_id is not None


def test_blocked_without_override_rejected():
    record = route_human_control(
        _proposal(),
        verdict=_verdict(AutonomyLevel.BLOCKED),
        at="2026-08-19T01:00:00Z",
    )
    assert record.path is ControlPath.REJECTED


def test_delegation_and_override_are_distinct_records():
    approval = route_human_control(
        _proposal(),
        verdict=_verdict(AutonomyLevel.APPROVED),
        review_decision=HumanReviewDecision(decision="approve", ruled_by="manager", at="2026-08-19T01:00:00Z"),
        reviewer_id="manager",
        at="2026-08-19T01:00:00Z",
    )
    override = route_human_control(
        _proposal(),
        verdict=_verdict(AutonomyLevel.HUMAN_REVIEW),
        review_decision=HumanReviewDecision(decision="override", ruled_by="senior", at="2026-08-19T01:00:00Z"),
        senior_id="vp",
        at="2026-08-19T01:00:00Z",
    )
    assert approval.path is ControlPath.APPROVAL
    assert override.path is ControlPath.OVERRIDE


def test_invalid_review_decision():
    with pytest.raises(HumanControlError):
        HumanReviewDecision(decision="cancel", ruled_by="x", at="t")
