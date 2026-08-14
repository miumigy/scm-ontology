"""Explicit semantic bridges between Order and planning quantities."""
from __future__ import annotations

from dataclasses import dataclass


class OrderPlanningBridgeError(ValueError):
    """Raised when an Order planning bridge is invalid."""


@dataclass(frozen=True)
class OrderPlanningBridge:
    """A typed semantic relation between an Order and a planning quantity."""

    order_type: str
    predicate: str
    planning_type: str

    def __post_init__(self) -> None:
        if not self.order_type.strip():
            raise OrderPlanningBridgeError("order_type must be non-empty")
        if not self.predicate.strip():
            raise OrderPlanningBridgeError("predicate must be non-empty")
        if not self.planning_type.strip():
            raise OrderPlanningBridgeError("planning_type must be non-empty")


CANONICAL_ORDER_PLANNING_BRIDGES = (
    OrderPlanningBridge("CustomerOrder", "contributes_to", "Demand"),
    OrderPlanningBridge("PurchaseOrder", "creates", "Supply"),
    OrderPlanningBridge("ProductionOrder", "creates", "Supply"),
)


def is_order_planning_bridge(value: object) -> bool:
    return isinstance(value, OrderPlanningBridge)
