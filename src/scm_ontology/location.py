"""Canonical location concept for the SCM domain layer."""
from __future__ import annotations

from dataclasses import dataclass


class LocationConceptError(ValueError):
    """Raised when a canonical location is invalid."""


@dataclass(frozen=True)
class CanonicalLocation:
    """A canonical place or organizational point at which SCM activity is situated."""

    location_id: str
    location_type: str
    name: str

    def __post_init__(self) -> None:
        if not self.location_id.strip():
            raise LocationConceptError("location_id must be non-empty")
        if not self.location_type.strip():
            raise LocationConceptError("location_type must be non-empty")
        if not self.name.strip():
            raise LocationConceptError("name must be non-empty")


def is_location(value: object) -> bool:
    return isinstance(value, CanonicalLocation)
