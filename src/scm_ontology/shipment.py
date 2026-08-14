"""Canonical shipment concept for the SCM domain layer."""
from __future__ import annotations

from dataclasses import dataclass


class ShipmentConceptError(ValueError):
    """Raised when a canonical shipment is invalid."""


@dataclass(frozen=True)
class CanonicalShipment:
    """A physical movement or handoff of an Item between two Locations."""

    shipment_id: str
    item_id: str
    quantity: float
    unit: str
    origin_location_id: str
    destination_location_id: str

    def __post_init__(self) -> None:
        if not self.shipment_id.strip():
            raise ShipmentConceptError("shipment_id must be non-empty")
        if not self.item_id.strip():
            raise ShipmentConceptError("item_id must be non-empty")
        if self.quantity < 0:
            raise ShipmentConceptError("quantity must be non-negative")
        if not self.unit.strip():
            raise ShipmentConceptError("unit must be non-empty")
        if not self.origin_location_id.strip():
            raise ShipmentConceptError("origin_location_id must be non-empty")
        if not self.destination_location_id.strip():
            raise ShipmentConceptError("destination_location_id must be non-empty")
        if self.origin_location_id == self.destination_location_id:
            raise ShipmentConceptError("origin and destination must differ")


def is_shipment(value: object) -> bool:
    return isinstance(value, CanonicalShipment)
