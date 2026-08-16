"""Deterministic canonical Demand/Supply Gap business-question boundary."""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Iterable


class DemandSupplyGapError(ValueError):
    """Raised when an S327 input violates its canonical contract."""


@dataclass(frozen=True)
class DemandSupplyFact:
    product_id: str
    location_id: str
    quantity: float
    fact_class: str = "demand"
    unit: str = "unit"
    evidence_id: str | None = None
    provenance_id: str | None = None

    def __post_init__(self) -> None:
        if not self.product_id.strip() or not self.location_id.strip():
            raise DemandSupplyGapError("product_id and location_id must be non-empty")
        if not self.unit.strip():
            raise DemandSupplyGapError("unit must be non-empty")
        if self.fact_class not in {"demand", "supply"}:
            raise DemandSupplyGapError("fact_class must be demand or supply")
        if not isinstance(self.quantity, (int, float)) or isinstance(self.quantity, bool):
            raise DemandSupplyGapError("quantity must be numeric")


@dataclass(frozen=True)
class DemandSupplyGap:
    product_id: str
    location_id: str
    unit: str
    demand: float
    supply: float
    gap: float
    evidence_ids: tuple[str, ...]
    provenance_ids: tuple[str, ...]

    def to_mapping(self) -> dict[str, Any]:
        return {
            "product_id": self.product_id,
            "location_id": self.location_id,
            "unit": self.unit,
            "demand": self.demand,
            "supply": self.supply,
            "gap": self.gap,
            "evidence_ids": list(self.evidence_ids),
            "provenance_ids": list(self.provenance_ids),
        }


def resolve_demand_supply_gap(facts: Iterable[DemandSupplyFact]) -> tuple[DemandSupplyGap, ...]:
    """Aggregate canonical facts by explicit scope and compute demand minus supply."""
    groups: dict[tuple[str, str, str], dict[str, Any]] = {}
    for fact in facts:
        key = (fact.product_id, fact.location_id, fact.unit)
        group = groups.setdefault(key, {"demand": 0.0, "supply": 0.0, "evidence_ids": set(), "provenance_ids": set()})
        group[fact.fact_class] += fact.quantity
        if fact.evidence_id is not None:
            group["evidence_ids"].add(fact.evidence_id)
        if fact.provenance_id is not None:
            group["provenance_ids"].add(fact.provenance_id)
    return tuple(
        DemandSupplyGap(p, l, u, g["demand"], g["supply"], g["demand"] - g["supply"], tuple(sorted(g["evidence_ids"])), tuple(sorted(g["provenance_ids"])))
        for (p, l, u), g in sorted(groups.items())
    )


def demand_supply_gap_to_mapping(result: Iterable[DemandSupplyGap]) -> dict[str, Any]:
    return {"contract_version": "S327.1", "gaps": [gap.to_mapping() for gap in result]}


def demand_supply_gap_to_json(result: Iterable[DemandSupplyGap]) -> str:
    return json.dumps(demand_supply_gap_to_mapping(result), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
