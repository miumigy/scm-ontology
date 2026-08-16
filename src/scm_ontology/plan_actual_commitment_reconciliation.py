"""Deterministic reconciliation of explicit plan, actual, and commitment facts.

S332 is a read-only business-question boundary. It does not infer identity,
change plans, approve commitments, or mutate Canonical Truth.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Iterable


class ReconciliationError(ValueError):
    """Raised when an S332 input violates the canonical contract."""


@dataclass(frozen=True)
class ReconciliationFact:
    item_id: str
    period_start: str
    period_end: str
    quantity: float
    fact_class: str
    unit: str = "unit"
    evidence_id: str | None = None
    provenance_id: str | None = None

    def __post_init__(self) -> None:
        if not self.item_id.strip():
            raise ReconciliationError("item_id must be non-empty")
        if not self.period_start.strip() or not self.period_end.strip():
            raise ReconciliationError("period_start and period_end must be non-empty")
        if not self.unit.strip():
            raise ReconciliationError("unit must be non-empty")
        if self.fact_class not in {"plan", "actual", "commitment"}:
            raise ReconciliationError("fact_class must be plan, actual, or commitment")
        if not isinstance(self.quantity, (int, float)) or isinstance(self.quantity, bool):
            raise ReconciliationError("quantity must be numeric")


@dataclass(frozen=True)
class ReconciliationResult:
    item_id: str
    period_start: str
    period_end: str
    unit: str
    plan: float
    actual: float
    commitment: float
    actual_vs_plan: float
    commitment_vs_plan: float
    actual_vs_commitment: float
    evidence_ids: tuple[str, ...]
    provenance_ids: tuple[str, ...]

    def to_mapping(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "period_start": self.period_start,
            "period_end": self.period_end,
            "unit": self.unit,
            "plan": self.plan,
            "actual": self.actual,
            "commitment": self.commitment,
            "actual_vs_plan": self.actual_vs_plan,
            "commitment_vs_plan": self.commitment_vs_plan,
            "actual_vs_commitment": self.actual_vs_commitment,
            "evidence_ids": list(self.evidence_ids),
            "provenance_ids": list(self.provenance_ids),
        }


def resolve_plan_actual_commitment(
    facts: Iterable[ReconciliationFact],
) -> tuple[ReconciliationResult, ...]:
    """Aggregate explicit facts by item/period/unit and calculate variances."""
    groups: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    for fact in facts:
        key = (fact.item_id, fact.period_start, fact.period_end, fact.unit)
        group = groups.setdefault(
            key,
            {"plan": 0.0, "actual": 0.0, "commitment": 0.0, "evidence_ids": set(), "provenance_ids": set()},
        )
        group[fact.fact_class] += fact.quantity
        if fact.evidence_id is not None:
            group["evidence_ids"].add(fact.evidence_id)
        if fact.provenance_id is not None:
            group["provenance_ids"].add(fact.provenance_id)

    return tuple(
        ReconciliationResult(
            item_id=item_id,
            period_start=period_start,
            period_end=period_end,
            unit=unit,
            plan=group["plan"],
            actual=group["actual"],
            commitment=group["commitment"],
            actual_vs_plan=group["actual"] - group["plan"],
            commitment_vs_plan=group["commitment"] - group["plan"],
            actual_vs_commitment=group["actual"] - group["commitment"],
            evidence_ids=tuple(sorted(group["evidence_ids"])),
            provenance_ids=tuple(sorted(group["provenance_ids"])),
        )
        for (item_id, period_start, period_end, unit), group in sorted(groups.items())
    )


def reconciliation_to_mapping(result: Iterable[ReconciliationResult]) -> dict[str, Any]:
    return {"contract_version": "S332.1", "reconciliations": [item.to_mapping() for item in result]}


def reconciliation_to_json(result: Iterable[ReconciliationResult]) -> str:
    return json.dumps(reconciliation_to_mapping(result), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
