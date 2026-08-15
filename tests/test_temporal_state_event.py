import pytest

from scm_ontology.temporal_state_event import (
    Event,
    EventKind,
    State,
    TemporalAssertion,
    TemporalKind,
    TimeInterval,
)


def test_time_interval_rejects_reverse_order() -> None:
    with pytest.raises(ValueError, match="reversed"):
        TimeInterval("2026-02-01", "2026-01-01")


def test_effective_and_transaction_time_are_distinct() -> None:
    effective = TemporalAssertion(
        "t:effective",
        "inventory:1",
        TemporalKind.EFFECTIVE,
        TimeInterval("2026-01-01"),
    )
    transaction = TemporalAssertion(
        "t:transaction",
        "inventory:1",
        TemporalKind.TRANSACTION,
        TimeInterval("2026-02-01"),
    )
    assert effective.kind is not transaction.kind


def test_state_is_valid_over_an_interval() -> None:
    state = State(
        ref="state:1",
        subject_ref="inventory:1",
        state_type_ref="Available",
        valid_time=TimeInterval("2026-01-01", "2026-01-03"),
        recorded_at="2026-01-04",
    )
    assert state.valid_time.end == "2026-01-03"
    assert state.recorded_at == "2026-01-04"


def test_transition_event_requires_both_states() -> None:
    with pytest.raises(ValueError, match="transition events"):
        Event(
            ref="event:1",
            subject_ref="shipment:1",
            event_kind=EventKind.TRANSITION,
            occurred_at="2026-01-01T10:00:00",
            from_state_ref="state:in_transit",
        )


def test_transition_connects_state_change_without_becoming_state() -> None:
    event = Event(
        ref="event:2",
        subject_ref="shipment:1",
        event_kind=EventKind.TRANSITION,
        occurred_at="2026-01-01T10:00:00",
        from_state_ref="state:in_transit",
        to_state_ref="state:delivered",
    )
    assert event.is_transition is True
    assert event.from_state_ref != event.to_state_ref


def test_planned_time_is_not_actual_time() -> None:
    planned = TemporalAssertion(
        "t:planned",
        "shipment:1",
        TemporalKind.PLANNED,
        TimeInterval("2026-01-05"),
    )
    actual = TemporalAssertion(
        "t:actual",
        "shipment:1",
        TemporalKind.ACTUAL,
        TimeInterval("2026-01-07"),
    )
    assert planned.kind is not actual.kind
