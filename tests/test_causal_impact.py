import pytest

from scm_ontology.causal import CausalRule
from scm_ontology.causal_chain import propagate_chain
from scm_ontology.causal_impact import CausalImpactError, project_impact
from scm_ontology.simulation import Event


def make_chain():
    rules = {
        "R1": CausalRule("R1", "SUPPLIER_DELAY", "MATERIAL_SHORTAGE"),
        "R2": CausalRule("R2", "MATERIAL_SHORTAGE", "PRODUCTION_DELAY"),
    }
    return propagate_chain(
        Event("E0", "SUPPLIER_DELAY", 1, "SUP-A", {"magnitudeDays": 7}),
        rules,
        {1: "E1", 2: "E2"},
        max_depth=3,
    )


def test_projects_chain_with_full_lineage():
    result = project_impact(
        make_chain(),
        affected_entity_id="KPI-OTD",
        impact_type="KPI_IMPACT",
        magnitude=-0.15,
        unit="ratio",
    )

    assert result.source_event_id == "E0"
    assert result.terminal_event_id == "E2"
    assert result.causal_depth == 2
    assert result.affected_entity_id == "KPI-OTD"
    assert result.impact_type == "KPI_IMPACT"
    assert result.magnitude == -0.15
    assert result.unit == "ratio"
    assert result.causal_event_ids == ("E0", "E1", "E2")


def test_projection_is_deterministic():
    args = dict(
        affected_entity_id="RISK-SERVICE",
        impact_type="RISK_IMPACT",
        magnitude=0.4,
        unit="probability",
    )
    assert project_impact(make_chain(), **args) == project_impact(make_chain(), **args)


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"affected_entity_id": "", "impact_type": "KPI_IMPACT", "magnitude": 1, "unit": "ratio"}, "affected_entity_id"),
        ({"affected_entity_id": "KPI-1", "impact_type": "", "magnitude": 1, "unit": "ratio"}, "impact_type"),
        ({"affected_entity_id": "KPI-1", "impact_type": "KPI_IMPACT", "magnitude": 1, "unit": ""}, "unit"),
    ],
)
def test_required_impact_fields_are_validated(kwargs, message):
    with pytest.raises(CausalImpactError, match=message):
        project_impact(make_chain(), **kwargs)
