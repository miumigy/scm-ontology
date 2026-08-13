import pytest

from scm_ontology.simulation import Event, SimulationError, State
from scm_ontology.transition import (
    SUPPLIER_DELAY_LEAD_TIME_RULE,
    StateTransitionRule,
    apply_transition_rule,
)


def supplier_state():
    return State(
        "S-000",
        0,
        {"SUP-A": {"id": "SUP-A", "entityType": "Party", "partyType": "SUPPLIER", "leadTimeDays": 5}},
    )


def test_supplier_delay_transition_is_explicit_and_deterministic():
    event = Event("E-001", "SUPPLIER_DELAY", 7, "SUP-A", {"magnitudeDays": 7})
    first = apply_transition_rule(supplier_state(), event, SUPPLIER_DELAY_LEAD_TIME_RULE)
    second = apply_transition_rule(supplier_state(), event, SUPPLIER_DELAY_LEAD_TIME_RULE)
    assert first == second
    next_state, changes = first
    assert next_state.entities["SUP-A"]["leadTimeDays"] == 12
    assert changes["leadTimeDays"] == {"before": 5, "after": 12}


def test_transition_does_not_mutate_input_state():
    state = supplier_state()
    original = state.snapshot()
    event = Event("E-001", "SUPPLIER_DELAY", 7, "SUP-A", {"magnitudeDays": 7})
    apply_transition_rule(state, event, SUPPLIER_DELAY_LEAD_TIME_RULE)
    assert state.snapshot() == original


def test_transition_rule_rejects_wrong_event_type():
    event = Event("E-001", "DEMAND_SPIKE", 7, "SUP-A", {"magnitudeDays": 7})
    with pytest.raises(SimulationError, match="cannot consume"):
        apply_transition_rule(supplier_state(), event, SUPPLIER_DELAY_LEAD_TIME_RULE)


def test_transition_rule_rejects_non_supplier_entity():
    state = State("S-000", 0, {"X": {"id": "X", "entityType": "Material", "leadTimeDays": 5}})
    event = Event("E-001", "SUPPLIER_DELAY", 7, "X", {"magnitudeDays": 7})
    with pytest.raises(SimulationError, match="requires Party"):
        apply_transition_rule(state, event, SUPPLIER_DELAY_LEAD_TIME_RULE)


def test_transition_rule_rejects_negative_magnitude():
    event = Event("E-001", "SUPPLIER_DELAY", 7, "SUP-A", {"magnitudeDays": -1})
    with pytest.raises(SimulationError, match="non-negative"):
        apply_transition_rule(supplier_state(), event, SUPPLIER_DELAY_LEAD_TIME_RULE)


def test_transition_rule_is_not_tied_to_a_specific_entity_id():
    state = State("S-000", 0, {"SUP-B": {"id": "SUP-B", "entityType": "Party", "partyType": "SUPPLIER", "leadTimeDays": 3}})
    event = Event("E-002", "SUPPLIER_DELAY", 4, "SUP-B", {"magnitudeDays": 2})
    next_state, changes = apply_transition_rule(state, event, SUPPLIER_DELAY_LEAD_TIME_RULE)
    assert next_state.entities["SUP-B"]["leadTimeDays"] == 5
    assert changes["leadTimeDays"] == {"before": 3, "after": 5}
