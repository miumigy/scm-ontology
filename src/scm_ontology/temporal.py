"""Canonical temporal primitives for SCM semantics."""
from __future__ import annotations

from dataclasses import dataclass


class TemporalConceptError(ValueError):
    """Raised when a canonical temporal primitive is invalid."""


@dataclass(frozen=True)
class CanonicalDuration:
    """A non-negative temporal magnitude with an explicit unit."""

    value: float
    unit: str

    def __post_init__(self) -> None:
        if self.value < 0:
            raise TemporalConceptError("duration value must be non-negative")
        if not self.unit.strip():
            raise TemporalConceptError("duration unit must be non-empty")


@dataclass(frozen=True)
class CanonicalTimeInterval:
    """A temporal interval represented by explicit start and end references."""

    start: str
    end: str

    def __post_init__(self) -> None:
        if not self.start.strip():
            raise TemporalConceptError("interval start must be non-empty")
        if not self.end.strip():
            raise TemporalConceptError("interval end must be non-empty")


def is_duration(value: object) -> bool:
    return isinstance(value, CanonicalDuration)


def is_time_interval(value: object) -> bool:
    return isinstance(value, CanonicalTimeInterval)
