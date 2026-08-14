"""Canonical demand concept for the SCM domain layer."""
from __future__ import annotations

from dataclasses import dataclass


class DemandConceptError(ValueError):
    """Raised when a canonical demand is invalid."""


@dataclass(frozen=True)
class CanonicalDemand:
    """A requirement for a quantity of an Item over a defined time scope."""

    item_id: str
    quantity: float
    unit: str
    period_start: str
    period_end: str
    demand_type: str = "requirement"

    def __post_init__(self) -> None:
        if not self.item_id.strip():
            raise DemandConceptError("item_id must be non-empty")
        if self.quantity < 0:
            raise DemandConceptError("quantity must be non-negative")
        if not self.unit.strip():
            raise DemandConceptError("unit must be non-empty")
        if not self.period_start.strip():
            raise DemandConceptError("period_start must be non-empty")
        if not self.period_end.strip():
            raise DemandConceptError("period_end must be non-empty")
        if not self.demand_type.strip():
            raise DemandConceptError("demand_type must be non-empty")
        if self.period_end < self.period_start:
            raise DemandConceptError("period_end must not precede period_start")


def is_demand(value: object) -> bool:
    return isinstance(value, CanonicalDemand)
