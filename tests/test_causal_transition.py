import pytest

from scm_ontology.causal import CausalRule
from scm_ontology.causal_transition import CausalTransitionError, derive_and_transition
from scm_ontology.simulation import Event, SimulationKernel, State


def supplier_state():
    return State(
        "S-000",
        0,
        {"SUP-A": {"id": "SUP-A", "entityType": "Party", "partyType": "SUPPLIER", "leadTimeDays": 5}},
    )


def delay_rule():
    return CausalRule(
        "CAUSE-SUPPLIER-DELAY",
        "SUPPLIER_DELAY",
        "SUPPLIER_DELAY",
    )


def test_derived_event_can_feed_existing_transition_kernel():
    source = Event("E-001", "SUPPLIER_DELAY", 7, "SUP-A", {"magnitudeDays": 7})
    result = derive_and_transition(
        supplier_state(), source, delay_rule(), "E-002", SimulationKernel()
    )

    assert result.source_event.event_id == "E-001"
    assert result.derived_event.event_id == "E-002"
    assert result.derived_event.provenance is not None
    assert result.derived_event.provenance.caused_by_event_id == "E-001"
    assert result.derived_event.provenance.rule_id == "CAUSE-SUPPLIER-DELAY"
    assert result.state.entities["SUP-A"]["leadTimeDays"] == 12
    assert result.transition.event_id == "E-002"


def test_causal_bridge_does_not_mutate_input_state():
    state = supplier_state()
    original = state.snapshot()
    source = Event("E-001", "SUPPLIER_DELAY", 7, "SUP-A", {"magnitudeDays": 7})
    derive_and_transition(state, source, delay_rule(), "E-002", SimulationKernel())
    assert state.snapshot() == original


def test_causal_bridge_wraps_transition_failure():
    source = Event("E-001", "SUPPLIER_DELAY", 7, "SUP-A", {"magnitudeDays": 7})
    rule = CausalRule("CAUSE-UNKNOWN", "SUPPLIER_DELAY", "DEMAND_SPIKE")
    with pytest.raises(CausalTransitionError, match="cannot transition state"):
        derive_and_transition(supplier_state(), source, rule, "E-002", SimulationKernel())
