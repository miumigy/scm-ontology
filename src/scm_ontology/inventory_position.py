"""Deterministic canonical Inventory Position business-question boundary.

S326 deliberately operates on already-canonical inventory facts. It does not
perform identity resolution, source mapping, inference, allocation, or graph
mutation. The result is a derived read-only answer with explicit source
lineage supplied by the caller.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Iterable


class InventoryPositionError(ValueError):
    """Raised when an inventory-position input violates the contract."""


@dataclass(frozen=True)
class InventoryPositionRecord:
    """Canonical inventory quantity for one product/location/quantity class."""

    product_id: str
    location_id: str
    quantity: float
    quantity_class: str = "on_hand"
    unit: str = "unit"
    evidence_id: str | None = None
    provenance_id: str | None = None

    def __post_init__(self) -> None:
        if not self.product_id.strip():
            raise InventoryPositionError("product_id must be non-empty")
        if not self.location_id.strip():
            raise InventoryPositionError("location_id must be non-empty")
        if not self.unit.strip():
            raise InventoryPositionError("unit must be non-empty")
        if self.quantity_class not in {"on_hand", "inbound", "outbound"}:
            raise InventoryPositionError(
                "quantity_class must be on_hand, inbound, or outbound"
            )
        if not isinstance(self.quantity, (int, float)) or isinstance(self.quantity, bool):
            raise InventoryPositionError("quantity must be numeric")


@dataclass(frozen=True)
class InventoryPosition:
    """Derived inventory position for a product/location/unit scope."""

    product_id: str
    location_id: str
    unit: str
    on_hand: float
    inbound: float
    outbound: float
    available: float
    evidence_ids: tuple[str, ...]
    provenance_ids: tuple[str, ...]

    def to_mapping(self) -> dict[str, Any]:
        return {
            "product_id": self.product_id,
            "location_id": self.location_id,
            "unit": self.unit,
            "on_hand": self.on_hand,
            "inbound": self.inbound,
            "outbound": self.outbound,
            "available": self.available,
            "evidence_ids": list(self.evidence_ids),
            "provenance_ids": list(self.provenance_ids),
        }


def resolve_inventory_position(
    records: Iterable[InventoryPositionRecord],
) -> tuple[InventoryPosition, ...]:
    """Resolve deterministic inventory positions from explicit canonical facts.

    ``available = on_hand + inbound - outbound``. Missing quantity classes are
    treated as zero. Records are grouped only by their explicit canonical
    product/location/unit keys; no source identity matching is attempted.
    """
    groups: dict[tuple[str, str, str], dict[str, Any]] = {}
    for record in records:
        key = (record.product_id, record.location_id, record.unit)
        group = groups.setdefault(
            key,
            {
                "on_hand": 0.0,
                "inbound": 0.0,
                "outbound": 0.0,
                "evidence_ids": set(),
                "provenance_ids": set(),
            },
        )
        group[record.quantity_class] += record.quantity
        if record.evidence_id is not None:
            group["evidence_ids"].add(record.evidence_id)
        if record.provenance_id is not None:
            group["provenance_ids"].add(record.provenance_id)

    result = []
    for (product_id, location_id, unit), group in sorted(groups.items()):
        result.append(
            InventoryPosition(
                product_id=product_id,
                location_id=location_id,
                unit=unit,
                on_hand=group["on_hand"],
                inbound=group["inbound"],
                outbound=group["outbound"],
                available=group["on_hand"] + group["inbound"] - group["outbound"],
                evidence_ids=tuple(sorted(group["evidence_ids"])),
                provenance_ids=tuple(sorted(group["provenance_ids"])),
            )
        )
    return tuple(result)


def inventory_position_to_mapping(
    result: Iterable[InventoryPosition],
) -> dict[str, Any]:
    """Return the deterministic JSON-safe S326 answer mapping."""
    positions = tuple(result)
    return {"contract_version": "S326.1", "positions": [p.to_mapping() for p in positions]}


def inventory_position_to_json(result: Iterable[InventoryPosition]) -> str:
    """Serialize an S326 result deterministically and UTF-8 safely."""
    return json.dumps(
        inventory_position_to_mapping(result),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
