"""Deterministic canonical Supplier Delay Impact business-question boundary.

S328 consumes already-canonical supplier commitment and delay facts. It derives
schedule impact without identity resolution, allocation, optimization, graph
mutation, or business-policy decisions.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Iterable


class SupplierDelayImpactError(ValueError):
    """Raised when an S328 input violates its canonical contract."""


@dataclass(frozen=True)
class SupplierCommitment:
    """Canonical supplier commitment for an explicit item/period scope."""

    supplier_id: str
    item_id: str
    committed_at: str
    promised_at: str
    unit: str = "unit"
    evidence_id: str | None = None
    provenance_id: str | None = None

    def __post_init__(self) -> None:
        if not self.supplier_id.strip() or not self.item_id.strip():
            raise SupplierDelayImpactError("supplier_id and item_id must be non-empty")
        if not self.committed_at.strip() or not self.promised_at.strip():
            raise SupplierDelayImpactError("committed_at and promised_at must be non-empty")
        if self.promised_at < self.committed_at:
            raise SupplierDelayImpactError("promised_at must not precede committed_at")
        if not self.unit.strip():
            raise SupplierDelayImpactError("unit must be non-empty")


@dataclass(frozen=True)
class SupplierDelayEvent:
    """Canonical observed delay for one supplier/item commitment scope."""

    supplier_id: str
    item_id: str
    expected_at: str
    actual_at: str
    unit: str = "unit"
    evidence_id: str | None = None
    provenance_id: str | None = None

    def __post_init__(self) -> None:
        if not self.supplier_id.strip() or not self.item_id.strip():
            raise SupplierDelayImpactError("supplier_id and item_id must be non-empty")
        if not self.expected_at.strip() or not self.actual_at.strip():
            raise SupplierDelayImpactError("expected_at and actual_at must be non-empty")
        if self.actual_at < self.expected_at:
            raise SupplierDelayImpactError("actual_at must not precede expected_at")
        if not self.unit.strip():
            raise SupplierDelayImpactError("unit must be non-empty")


@dataclass(frozen=True)
class SupplierDelayImpact:
    """Derived supplier delay observation for an explicit commitment scope."""

    supplier_id: str
    item_id: str
    unit: str
    committed_at: str
    promised_at: str
    expected_at: str
    actual_at: str
    delay_days: int
    evidence_ids: tuple[str, ...]
    provenance_ids: tuple[str, ...]

    def to_mapping(self) -> dict[str, Any]:
        return {
            "supplier_id": self.supplier_id,
            "item_id": self.item_id,
            "unit": self.unit,
            "committed_at": self.committed_at,
            "promised_at": self.promised_at,
            "expected_at": self.expected_at,
            "actual_at": self.actual_at,
            "delay_days": self.delay_days,
            "evidence_ids": list(self.evidence_ids),
            "provenance_ids": list(self.provenance_ids),
        }


def _date_delta_days(start: str, end: str) -> int:
    from datetime import date

    try:
        return (date.fromisoformat(end[:10]) - date.fromisoformat(start[:10])).days
    except ValueError as exc:
        raise SupplierDelayImpactError("timestamps must begin with ISO dates") from exc


def resolve_supplier_delay_impact(
    commitments: Iterable[SupplierCommitment],
    delays: Iterable[SupplierDelayEvent],
) -> tuple[SupplierDelayImpact, ...]:
    """Match only explicit canonical supplier/item/unit keys and derive delay.

    The runtime never infers supplier or item identity. A delay without an exact
    canonical commitment scope is ignored rather than implicitly attached.
    """
    commitment_map = {
        (c.supplier_id, c.item_id, c.unit): c
        for c in commitments
    }
    result: list[SupplierDelayImpact] = []
    for event in delays:
        key = (event.supplier_id, event.item_id, event.unit)
        commitment = commitment_map.get(key)
        if commitment is None:
            continue
        delay_days = max(_date_delta_days(event.expected_at, event.actual_at), 0)
        evidence_ids = tuple(sorted(x for x in (commitment.evidence_id, event.evidence_id) if x is not None))
        provenance_ids = tuple(sorted(x for x in (commitment.provenance_id, event.provenance_id) if x is not None))
        result.append(
            SupplierDelayImpact(
                supplier_id=event.supplier_id,
                item_id=event.item_id,
                unit=event.unit,
                committed_at=commitment.committed_at,
                promised_at=commitment.promised_at,
                expected_at=event.expected_at,
                actual_at=event.actual_at,
                delay_days=delay_days,
                evidence_ids=evidence_ids,
                provenance_ids=provenance_ids,
            )
        )
    return tuple(sorted(result, key=lambda x: (x.supplier_id, x.item_id, x.unit, x.expected_at, x.actual_at)))


def supplier_delay_impact_to_mapping(result: Iterable[SupplierDelayImpact]) -> dict[str, Any]:
    return {"contract_version": "S328.1", "impacts": [x.to_mapping() for x in result]}


def supplier_delay_impact_to_json(result: Iterable[SupplierDelayImpact]) -> str:
    return json.dumps(
        supplier_delay_impact_to_mapping(result),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
