import pytest

from scm_ontology.causal import CausalRule
from scm_ontology.causal_chain import propagate_chain
from scm_ontology.causal_impact import project_impact
from scm_ontology.impact_target import ImpactTargetError, bind_impact_target
from scm_ontology.simulation import Event


def make_impact():
    chain = propagate_chain(
        Event("E0", "SUPPLIER_DELAY", 1, "SUP-A", {"magnitudeDays": 7}),
        {"R1": CausalRule("R1", "SUPPLIER_DELAY", "MATERIAL_SHORTAGE")},
        {1: "E1"},
    )
    return project_impact(chain, "KPI-OTD", "KPI_IMPACT", -0.15, "ratio")


def test_binds_impact_to_semantic_target_without_mutating_impact():
    impact = make_impact()
    target = bind_impact_target(impact, "OTD", "KPI", "kpi:on_time_delivery")
    assert target.target_id == "OTD"
    assert target.target_type == "KPI"
    assert target.impact_type == "KPI_IMPACT"
    assert target.semantic_ref == "kpi:on_time_delivery"
    assert impact.affected_entity_id == "KPI-OTD"


def test_binding_is_deterministic():
    impact = make_impact()
    args = ("OTD", "KPI", "kpi:on_time_delivery")
    assert bind_impact_target(impact, *args) == bind_impact_target(impact, *args)


@pytest.mark.parametrize(
    "target_id,target_type,semantic_ref,message",
    [
        ("", "KPI", "kpi:otd", "target_id"),
        ("OTD", "", "kpi:otd", "target_type"),
        ("OTD", "KPI", "", "semantic_ref"),
    ],
)
def test_required_target_fields_are_validated(target_id, target_type, semantic_ref, message):
    with pytest.raises(ImpactTargetError, match=message):
        bind_impact_target(make_impact(), target_id, target_type, semantic_ref)
