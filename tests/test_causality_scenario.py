import pytest

from scm_ontology.causality_scenario import (
    CausalRelationKind,
    CausalRelationship,
    Counterfactual,
    Scenario,
    ScenarioChange,
    ScenarioKind,
)


def test_causal_relationship_requires_distinct_cause_and_effect() -> None:
    with pytest.raises(ValueError, match="distinct"):
        CausalRelationship("c:1", "x", "x", CausalRelationKind.CAUSES)


def test_causal_relationship_can_carry_evidence_and_uncertainty() -> None:
    relation = CausalRelationship(
        "c:1", "stockout", "expedite", CausalRelationKind.CONTRIBUTES_TO,
        evidence_refs=("e:1",), uncertainty_ref="u:1",
    )
    assert relation.evidence_refs == ("e:1",)
    assert relation.uncertainty_ref == "u:1"


def test_actual_world_is_not_a_scenario() -> None:
    with pytest.raises(ValueError, match="actual world"):
        Scenario("s:actual", ScenarioKind.ACTUAL, "world:actual", "actual")


def test_scenario_is_explicitly_anchored_to_parent_world() -> None:
    scenario = Scenario(
        "s:1", ScenarioKind.COUNTERFACTUAL, "world:actual", "no expedite intervention"
    )
    assert scenario.parent_world_ref == "world:actual"


def test_scenario_change_requires_a_real_difference() -> None:
    with pytest.raises(ValueError, match="different"):
        ScenarioChange("c:1", "s:1", "shipment:1", "eta", "v1", "v1")


def test_counterfactual_keeps_observed_and_alternative_outcomes_distinct() -> None:
    cf = Counterfactual(
        "cf:1", "s:1", "intervention:expedite", "outcome:actual", "outcome:alternative",
        causal_basis_refs=("cause:1",),
    )
    assert cf.observed_outcome_ref != cf.counterfactual_outcome_ref
    assert cf.causal_basis_refs == ("cause:1",)
