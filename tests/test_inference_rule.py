import pytest

from scm_ontology.inference_rule import InferenceRule


def test_rule_maps_premises_to_conclusion():
    rule = InferenceRule(
        rule_id="rule-delivered-available",
        premise_types=("ShipmentDelivered",),
        conclusion_type="InventoryAvailable",
    )
    assert rule.rule_id == "rule-delivered-available"
    assert rule.premise_types == ("ShipmentDelivered",)
    assert rule.conclusion_type == "InventoryAvailable"


def test_rule_can_have_multiple_premises():
    rule = InferenceRule(
        rule_id="rule-feasible",
        premise_types=("CapacityAvailable", "DemandExists"),
        conclusion_type="SupplyFeasible",
    )
    assert len(rule.premise_types) == 2


def test_rule_rejects_empty_identity_and_semantics():
    with pytest.raises(ValueError):
        InferenceRule("", ("Fact",), "Conclusion")
    with pytest.raises(ValueError):
        InferenceRule("r1", (), "Conclusion")
    with pytest.raises(ValueError):
        InferenceRule("r1", ("Fact",), "")


def test_rule_does_not_execute_inference():
    rule = InferenceRule("r1", ("Fact",), "Conclusion")
    assert not hasattr(rule, "infer")
    assert not hasattr(rule, "evaluate")
