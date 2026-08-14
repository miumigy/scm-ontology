"""Canonical order concept for the SCM domain layer."""
from __future__ import annotations

from dataclasses import dataclass


class OrderConceptError(ValueError):
    """Raised when a canonical order is invalid."""


@dataclass(frozen=True)
class CanonicalOrder:
    """A commitment or request concerning a quantity of an Item."""

    order_id: str
    item_id: str
    quantity: float
    unit: str
    order_type: str = "request"

    def __post_init__(self) -> None:
        if not self.order_id.strip():
            raise OrderConceptError("order_id must be non-empty")
        if not self.item_id.strip():
            raise OrderConceptError("item_id must be non-empty")
        if self.quantity < 0:
            raise OrderConceptError("quantity must be non-negative")
        if not self.unit.strip():
            raise OrderConceptError("unit must be non-empty")
        if not self.order_type.strip():
            raise OrderConceptError("order_type must be non-empty")


def is_order(value: object) -> bool:
    return isinstance(value, CanonicalOrder)
