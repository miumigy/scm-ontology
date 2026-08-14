"""Canonical supply concept for the SCM domain layer."""
from __future__ import annotations

from dataclasses import dataclass


class SupplyConceptError(ValueError):
    """Raised when a canonical supply is invalid."""


@dataclass(frozen=True)
class CanonicalSupply:
    """A quantity of an Item that is planned or expected to become supply."""

    item_id: str
    quantity: float
    unit: str
    period_start: str
    period_end: str
    supply_type: str = "planned"

    def __post_init__(self) -> None:
        if not self.item_id.strip():
            raise SupplyConceptError("item_id must be non-empty")
        if self.quantity < 0:
            raise SupplyConceptError("quantity must be non-negative")
        if not self.unit.strip():
            raise SupplyConceptError("unit must be non-empty")
        if not self.period_start.strip():
            raise SupplyConceptError("period_start must be non-empty")
        if not self.period_end.strip():
            raise SupplyConceptError("period_end must be non-empty")
        if not self.supply_type.strip():
            raise SupplyConceptError("supply_type must be non-empty")
        if self.period_end < self.period_start:
            raise SupplyConceptError("period_end must not precede period_start")


def is_supply(value: object) -> bool:
    return isinstance(value, CanonicalSupply)
