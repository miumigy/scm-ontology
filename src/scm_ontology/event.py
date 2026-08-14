"""Canonical event concept for the SCM domain layer."""
from __future__ import annotations

from dataclasses import dataclass


class EventConceptError(ValueError):
    """Raised when a canonical event is invalid."""


@dataclass(frozen=True)
class CanonicalEvent:
    """A fact that an event of a given type occurred for a subject."""

    event_id: str
    event_type: str
    occurred_at: str
    subject_id: str

    def __post_init__(self) -> None:
        if not self.event_id.strip():
            raise EventConceptError("event_id must be non-empty")
        if not self.event_type.strip():
            raise EventConceptError("event_type must be non-empty")
        if not self.occurred_at.strip():
            raise EventConceptError("occurred_at must be non-empty")
        if not self.subject_id.strip():
            raise EventConceptError("subject_id must be non-empty")


def is_event(value: object) -> bool:
    return isinstance(value, CanonicalEvent)
