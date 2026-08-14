import pytest

from scm_ontology.event_state_transition import (
    CANONICAL_EVENT_STATE_TRANSITIONS,
    EventStateTransition,
    EventStateTransitionError,
    is_event_state_transition,
)


def test_canonical_event_state_transitions_are_explicit():
    transitions = {
        (t.event_type, t.predicate, t.state_type)
        for t in CANONICAL_EVENT_STATE_TRANSITIONS
    }
    assert transitions == {
        ("shipment_departed", "establishes", "in_transit"),
        ("shipment_arrived", "establishes", "arrived"),
        ("order_confirmed", "establishes", "confirmed"),
        ("production_started", "establishes", "running"),
        ("production_completed", "establishes", "completed"),
    }
    assert all(is_event_state_transition(t) for t in CANONICAL_EVENT_STATE_TRANSITIONS)


@pytest.mark.parametrize(
    "kwargs,message",
    [
        ({"event_type": "", "predicate": "establishes", "state_type": "arrived"}, "event_type"),
        ({"event_type": "shipment_arrived", "predicate": "", "state_type": "arrived"}, "predicate"),
        ({"event_type": "shipment_arrived", "predicate": "establishes", "state_type": ""}, "state_type"),
    ],
)
def test_rejects_invalid_transition(kwargs, message):
    with pytest.raises(EventStateTransitionError, match=message):
        EventStateTransition(**kwargs)
