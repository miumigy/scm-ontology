import pytest

from scm_ontology.s131_causal_reasoning import (
    CausalAssessmentResult,
    CausalClaim,
    assess_claim,
)


def claim(scenario_ref=None):
    return CausalClaim(
        ref="claim:c1",
        cause_ref="event:cause",
        effect_ref="outcome:effect",
        relationship_ref="causal:1",
        scenario_ref=scenario_ref,
    )


def test_supported_claim_requires_evidence() -> None:
    with pytest.raises(ValueError):
        assess_claim(claim(), result=CausalAssessmentResult.SUPPORTED)


def test_attribution_does_not_substitute_for_causal_evidence() -> None:
    with pytest.raises(ValueError):
        assess_claim(
            claim(),
            result=CausalAssessmentResult.SUPPORTED,
            attribution_ref="attribution:1",
        )


def test_uncertain_claim_is_not_supported() -> None:
    assessment = assess_claim(
        claim(),
        result=CausalAssessmentResult.UNCERTAIN,
        evidence_refs=("evidence:1",),
    )
    assert assessment.result is CausalAssessmentResult.UNCERTAIN
    assert assessment.is_decision is False


def test_counterfactual_assessment_is_scenario_scoped() -> None:
    assessment = assess_claim(
        claim("scenario:counterfactual-1"),
        result=CausalAssessmentResult.SUPPORTED,
        evidence_refs=("evidence:scenario",),
    )
    assert assessment.is_counterfactual is True
    assert assessment.scenario_ref == "scenario:counterfactual-1"


def test_cause_and_effect_must_differ() -> None:
    with pytest.raises(ValueError):
        CausalClaim(
            ref="claim:c2",
            cause_ref="same",
            effect_ref="same",
            relationship_ref="causal:2",
        )
