from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Optional


class TemporalKind(StrEnum):
    EFFECTIVE = "effective"
    TRANSACTION = "transaction"
    OBSERVATION = "observation"
    PLANNED = "planned"
    SCHEDULED = "scheduled"
    ACTUAL = "actual"


class EventKind(StrEnum):
    OCCURRENCE = "occurrence"
    TRANSITION = "transition"
    OBSERVATION = "observation"


@dataclass(frozen=True)
class TimeInterval:
    start: str
    end: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.start:
            raise ValueError("time interval requires start")
        if self.end is not None and self.start > self.end:
            raise ValueError("time interval is reversed")


@dataclass(frozen=True)
class TemporalAssertion:
    ref: str
    subject_ref: str
    kind: TemporalKind
    interval: TimeInterval
    source_ref: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.ref or not self.subject_ref:
            raise ValueError("ref and subject_ref are required")


@dataclass(frozen=True)
class State:
    ref: str
    subject_ref: str
    state_type_ref: str
    valid_time: TimeInterval
    recorded_at: Optional[str] = None
    provenance_ref: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.ref or not self.subject_ref or not self.state_type_ref:
            raise ValueError("ref, subject_ref, and state_type_ref are required")


@dataclass(frozen=True)
class Event:
    ref: str
    subject_ref: str
    event_kind: EventKind
    occurred_at: str
    from_state_ref: Optional[str] = None
    to_state_ref: Optional[str] = None
    observation_ref: Optional[str] = None
    provenance_ref: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.ref or not self.subject_ref or not self.occurred_at:
            raise ValueError("ref, subject_ref, and occurred_at are required")
        if self.event_kind is EventKind.TRANSITION:
            if not self.from_state_ref or not self.to_state_ref:
                raise ValueError("transition events require from_state_ref and to_state_ref")

    @property
    def is_transition(self) -> bool:
        return self.event_kind is EventKind.TRANSITION
