import pytest

from scm_ontology.s133_decision_reasoning import (
    Alternative,
    Decision,
    DecisionEvaluation,
    Recommendation,
    create_decision,
    create_recommendation,
)


def evaluation() -> DecisionEvaluation:
    return DecisionEvaluation(
        ref="evaluation:1",
        alternative_refs=("alternative:a", "alternative:b"),
        objective_refs=("objective:service",),
        constraint_refs=("constraint:capacity",),
        policy_refs=("policy:priority",),
        evidence_refs=("evidence:1",),
        epistemic_status="mixed",
    )


def test_recommendation_is_not_decision() -> None:
    recommendation = create_recommendation(
        ref="recommendation:1",
        selected_alternative_ref="alternative:a",
        evaluation_ref="evaluation:1",
        rationale="Best feasible trade-off",
        uncertainty="medium",
    )
    assert recommendation.is_decision is False


def test_decision_requires_authority() -> None:
    with pytest.raises(ValueError):
        create_decision(
            ref="decision:1",
            selected_alternative_ref="alternative:a",
            evaluation_ref="evaluation:1",
            authority_ref="",
            decided_at="2026-08-15T10:00:00Z",
        )


def test_decision_is_distinct_from_recommendation() -> None:
    recommendation = Recommendation(
        ref="recommendation:1",
        selected_alternative_ref="alternative:a",
        evaluation_ref="evaluation:1",
    )
    decision = create_decision(
        ref="decision:1",
        selected_alternative_ref="alternative:a",
        evaluation_ref="evaluation:1",
        authority_ref="actor:planner",
        decided_at="2026-08-15T10:00:00Z",
        recommendation_ref=recommendation.ref,
    )
    assert decision.is_recommendation is False
    assert decision.recommendation_ref == recommendation.ref


def test_evaluation_requires_alternative() -> None:
    with pytest.raises(ValueError):
        DecisionEvaluation(ref="evaluation:empty", alternative_refs=())


def test_alternative_can_carry_reasoning_references() -> None:
    alternative = Alternative(
        ref="alternative:a",
        label="Increase production capacity",
        constraint_evaluation_refs=("evaluation:constraint",),
        what_if_result_refs=("whatif:capacity-up",),
        causal_assessment_refs=("assessment:capacity-effect",),
    )
    assert alternative.what_if_result_refs == ("whatif:capacity-up",)
