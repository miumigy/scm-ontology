"""Canonical temporal reference for SCM semantics."""
from __future__ import annotations

from dataclasses import dataclass


class TimeReferenceError(ValueError):
    """Raised when a canonical time reference is invalid."""


@dataclass(frozen=True)
class CanonicalTimeReference:
    """A typed temporal reference with an explicit semantic basis."""

    value: str
    time_type: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise TimeReferenceError("value must be non-empty")
        if not self.time_type.strip():
            raise TimeReferenceError("time_type must be non-empty")


CANONICAL_TIME_TYPES = (
    "occurred_at",
    "effective_at",
    "planned_at",
    "requested_at",
    "confirmed_at",
)


def is_time_reference(value: object) -> bool:
    return isinstance(value, CanonicalTimeReference)
