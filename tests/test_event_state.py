from scm_ontology.event_state import CanonicalEvent, CanonicalState


def test_event_is_an_occurrence_with_semantic_type():
    event = CanonicalEvent(event_id="E1", event_type="shipment_departed")
    assert event.event_id == "E1"
    assert event.event_type == "shipment_departed"


def test_state_is_a_condition_of_a_subject():
    state = CanonicalState(
        state_id="S1", state_type="in_transit", subject_id="Shipment-1"
    )
    assert state.state_id == "S1"
    assert state.state_type == "in_transit"
    assert state.subject_id == "Shipment-1"


def test_event_does_not_embed_state_transition_semantics():
    event = CanonicalEvent(event_id="E1", event_type="shipment_departed")
    assert not hasattr(event, "state_id")
    assert not hasattr(event, "causes")


def test_state_does_not_embed_event_or_temporal_persistence_policy():
    state = CanonicalState(state_id="S1", state_type="available", subject_id="Item-1")
    assert not hasattr(state, "event_id")
    assert not hasattr(state, "valid_from")
    assert not hasattr(state, "valid_to")
