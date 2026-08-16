"""Deterministic canonical Demand/Supply Gap business-question boundary.

S327 deliberately operates on already-canonical demand and supply facts. It does
not perform identity resolution, source mapping, inference, allocation, graph
mutation, or business-policy decisions. The result is a derived read-only answer
with explicit source lineage supplied by the caller.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Iterable


class DemandSupplyGapError(ValueError):
    """Raised when a demand/supply-gap input violates the contract."""


@dataclass(frozen=True)
class DemandSupplyRecord:
    """Canonical demand or supply quantity for one item/period/unit scope."""

    item_id: str
    quantity: float
    kind: str = "demand"
    unit: str = "unit"
    period_start: str = ""
    period_end: str = ""
    evidence_id: str | None = None
    provenance_id: str | None = None

    def __post_init__(self) -> None:
        if not self.item_id.strip():
            raise DemandSupplyGapError("item_id must be non-empty")
        if not isinstance(self.quantity, (int, float)) or isinstance(self.quantity, bool):
            raise DemandSupplyGapError("quantity must be numeric")
        if self.quantity < 0:
            raise DemandSupplyGapError("quantity must be non-negative")
        if self.kind not in {"demand", "supply"}:
            raise DemandSupplyGapError("kind must be demand or supply")
        if not self.unit.strip():
            raise DemandSupplyGapError("unit must be non-empty")
        if not self.period_start.strip() or not self.period_end.strip():
            raise DemandSupplyGapError("period_start and period_end must be non-empty")
        if self.period_end < self.period_start:
            raise DemandSupplyGapError("period_end must not precede period_start")


@dataclass(frozen=True)
class DemandSupplyGap:
    """Derived demand/supply gap for an item/period/unit scope."""

    item_id: str
    unit: str
    period_start: str
    period_end: str
    demand: float
    supply: float
    gap: float
    evidence_ids: tuple[str, ...]
    provenance_ids: tuple[str, ...]

    def to_mapping(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "unit": self.unit,
            "period_start": self.period_start,
            "period_end": self.period_end,
            "demand": self.demand,
            "supply": self.supply,
            "gap": self.gap,
            "evidence_ids": list(self.evidence_ids),
            "provenance_ids": list(self.provenance_ids),
        }


def resolve_demand_supply_gap(
    records: Iterable[DemandSupplyRecord],
) -> tuple[DemandSupplyGap, ...]:
    """Resolve deterministic demand/supply gaps from explicit canonical facts.

    ``gap = max(demand - supply, 0)``. Missing demand or supply sides are treated
    as zero. Records are grouped only by their explicit canonical
    item/unit/period keys; no source identity matching or inference is attempted.
    """
    groups: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    for record in records:
        key = (
            record.item_id,
            record.unit,
            record.period_start,
            record.period_end,
        )
        group = groups.setdefault(
            key,
            {
                "demand": 0.0,
                "supply": 0.0,
                "evidence_ids": set(),
                "provenance_ids": set(),
            },
        )
        group[record.kind] += record.quantity
        if record.evidence_id is not None:
            group["evidence_ids"].add(record.evidence_id)
        if record.provenance_id is not None:
            group["provenance_ids"].add(record.provenance_id)

    result = []
    for (item_id, unit, period_start, period_end), group in sorted(groups.items()):
        demand = group["demand"]
        supply = group["supply"]
        result.append(
            DemandSupplyGap(
                item_id=item_id,
                unit=unit,
                period_start=period_start,
                period_end=period_end,
                demand=demand,
                supply=supply,
                gap=max(demand - supply, 0.0),
                evidence_ids=tuple(sorted(group["evidence_ids"])),
                provenance_ids=tuple(sorted(group["provenance_ids"])),
            )
        )
    return tuple(result)


def demand_supply_gap_to_mapping(
    result: Iterable[DemandSupplyGap],
) -> dict[str, Any]:
    """Return the deterministic JSON-safe S327 answer mapping."""
    gaps = tuple(result)
    return {
        "contract_version": "S327.1",
        "gaps": [g.to_mapping() for g in gaps],
    }


def demand_supply_gap_to_json(result: Iterable[DemandSupplyGap]) -> str:
    """Serialize an S327 result deterministically and UTF-8 safely."""
    return json.dumps(
        demand_supply_gap_to_mapping(result),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
