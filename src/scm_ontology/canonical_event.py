"""Canonical, framework-independent event semantics."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Mapping


class CanonicalEventError(ValueError):
    """Raised when a canonical event violates its semantic contract."""


@dataclass(frozen=True)
class CanonicalEvent:
    """An occurrence associated with an entity at a defined instant."""

    event_type: str
    occurred_at: datetime
    entity_id: str
    attributes: Mapping[str, object]

    def __post_init__(self) -> None:
        if not self.event_type:
            raise CanonicalEventError("event_type must be non-empty")
        if not isinstance(self.occurred_at, datetime):
            raise CanonicalEventError("occurred_at must be a datetime")
        if self.occurred_at.tzinfo is None or self.occurred_at.utcoffset() is None:
            raise CanonicalEventError("occurred_at must be timezone-aware")
        if not self.entity_id:
            raise CanonicalEventError("entity_id must be non-empty")
        if self.attributes is None:
            raise CanonicalEventError("attributes must be provided")


def is_event(value: object) -> bool:
    """Return whether a value is explicitly a CanonicalEvent."""
    return isinstance(value, CanonicalEvent)
