"""Explicit semantic bridge from Event occurrences to State conditions."""
from __future__ import annotations

from dataclasses import dataclass


class EventStateTransitionError(ValueError):
    """Raised when an Event-State transition contract is invalid."""


@dataclass(frozen=True)
class EventStateTransition:
    """A scoped relationship describing an event's state effect."""

    event_type: str
    predicate: str
    state_type: str

    def __post_init__(self) -> None:
        if not self.event_type.strip():
            raise EventStateTransitionError("event_type must be non-empty")
        if not self.predicate.strip():
            raise EventStateTransitionError("predicate must be non-empty")
        if not self.state_type.strip():
            raise EventStateTransitionError("state_type must be non-empty")


CANONICAL_EVENT_STATE_TRANSITIONS = (
    EventStateTransition("shipment_departed", "establishes", "in_transit"),
    EventStateTransition("shipment_arrived", "establishes", "arrived"),
    EventStateTransition("order_confirmed", "establishes", "confirmed"),
    EventStateTransition("production_started", "establishes", "running"),
    EventStateTransition("production_completed", "establishes", "completed"),
)


def is_event_state_transition(value: object) -> bool:
    return isinstance(value, EventStateTransition)
