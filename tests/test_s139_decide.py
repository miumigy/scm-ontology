import pytest

from scm_ontology.s139_decide import (
    Decision,
    DecisionDisposition,
    DecisionStatus,
    make_decision,
)


def test_decision_preserves_authority_and_evidence() -> None:
    decision = make_decision(
        ref="decision:1",
        subject_ref="network:1",
        decision_maker_ref="actor:planner",
        disposition=DecisionDisposition.SELECT,
        selected_alternative_refs=("alternative:a",),
        considered_alternative_refs=("alternative:a", "alternative:b"),
        evidence_refs=("observation:1",),
        reasoning_refs=("explanation:1",),
        status=DecisionStatus.APPROVED,
    )
    assert decision.decision_maker_ref == "actor:planner"
    assert decision.selected_alternative_refs == ("alternative:a",)
    assert decision.evidence_refs == ("observation:1",)


def test_recommendation_does_not_become_decision_implicitly() -> None:
    decision = make_decision(
        ref="decision:2",
        subject_ref="plan:1",
        decision_maker_ref="actor:manager",
        disposition=DecisionDisposition.AUTHORIZE,
        recommendation_refs=("recommendation:1",),
    )
    assert decision.recommendation_refs == ("recommendation:1",)
    assert decision.is_recommendation is False


def test_decision_is_not_action_or_outcome() -> None:
    decision = Decision(
        ref="decision:3",
        subject_ref="plan:1",
        decision_maker_ref="actor:manager",
        disposition=DecisionDisposition.SELECT,
    )
    assert decision.is_action is False
    assert decision.is_outcome is False


def test_scenario_decision_remains_scoped() -> None:
    decision = make_decision(
        ref="decision:scenario:1",
        subject_ref="network:1",
        decision_maker_ref="agent:simulation",
        disposition=DecisionDisposition.SELECT,
        scenario_ref="scenario:1",
    )
    assert decision.is_scenario_decision is True


def test_no_action_is_explicit_disposition() -> None:
    decision = make_decision(
        ref="decision:no-action",
        subject_ref="exception:1",
        decision_maker_ref="actor:manager",
        disposition=DecisionDisposition.NO_ACTION,
    )
    assert decision.disposition is DecisionDisposition.NO_ACTION


def test_decision_requires_maker() -> None:
    with pytest.raises(ValueError):
        Decision(
            ref="decision:bad",
            subject_ref="plan:1",
            decision_maker_ref="",
            disposition=DecisionDisposition.SELECT,
        )
