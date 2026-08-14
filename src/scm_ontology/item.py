"""Canonical item concept for the SCM domain layer."""
from __future__ import annotations

from dataclasses import dataclass


class ItemConceptError(ValueError):
    """Raised when a canonical item is invalid."""


@dataclass(frozen=True)
class CanonicalItem:
    """A definable thing that can be identified, planned, moved, transformed, or held."""

    item_id: str
    item_type: str
    name: str

    def __post_init__(self) -> None:
        if not self.item_id.strip():
            raise ItemConceptError("item_id must be non-empty")
        if not self.item_type.strip():
            raise ItemConceptError("item_type must be non-empty")
        if not self.name.strip():
            raise ItemConceptError("name must be non-empty")


def is_item(value: object) -> bool:
    return isinstance(value, CanonicalItem)
