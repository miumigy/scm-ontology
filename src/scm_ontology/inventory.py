"""Canonical inventory concept for the SCM domain layer."""
from __future__ import annotations

from dataclasses import dataclass


class InventoryConceptError(ValueError):
    """Raised when a canonical inventory concept is invalid."""


@dataclass(frozen=True)
class CanonicalInventory:
    """A quantity of a defined item held at a defined supply-chain entity."""

    item_id: str
    location_id: str
    quantity: float
    unit: str

    def __post_init__(self) -> None:
        if not self.item_id.strip():
            raise InventoryConceptError("item_id must be non-empty")
        if not self.location_id.strip():
            raise InventoryConceptError("location_id must be non-empty")
        if self.quantity < 0:
            raise InventoryConceptError("quantity must be non-negative")
        if not self.unit.strip():
            raise InventoryConceptError("unit must be non-empty")


def is_inventory(value: object) -> bool:
    return isinstance(value, CanonicalInventory)
