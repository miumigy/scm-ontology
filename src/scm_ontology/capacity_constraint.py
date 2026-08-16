"""Deterministic canonical capacity-constraint business-question boundary."""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Iterable


class CapacityConstraintError(ValueError):
    """Raised when an S330 input violates the canonical contract."""


@dataclass(frozen=True)
class CapacityFact:
    resource_id: str
    capacity: float
    unit: str = "unit"
    evidence_id: str | None = None
    provenance_id: str | None = None

    def __post_init__(self) -> None:
        if not self.resource_id.strip() or not self.unit.strip():
            raise CapacityConstraintError("resource_id and unit must be non-empty")
        if not isinstance(self.capacity, (int, float)) or isinstance(self.capacity, bool) or self.capacity < 0:
            raise CapacityConstraintError("capacity must be a non-negative number")


@dataclass(frozen=True)
class CapacityRequirement:
    resource_id: str
    quantity: float
    unit: str = "unit"
    evidence_id: str | None = None
    provenance_id: str | None = None

    def __post_init__(self) -> None:
        if not self.resource_id.strip() or not self.unit.strip():
            raise CapacityConstraintError("resource_id and unit must be non-empty")
        if not isinstance(self.quantity, (int, float)) or isinstance(self.quantity, bool) or self.quantity < 0:
            raise CapacityConstraintError("quantity must be a non-negative number")


@dataclass(frozen=True)
class CapacityConstraint:
    resource_id: str
    unit: str
    capacity: float
    required: float
    headroom: float
    utilization: float | None
    feasible: bool
    evidence_ids: tuple[str, ...]
    provenance_ids: tuple[str, ...]

    def to_mapping(self) -> dict[str, Any]:
        return {
            "resource_id": self.resource_id,
            "unit": self.unit,
            "capacity": self.capacity,
            "required": self.required,
            "headroom": self.headroom,
            "utilization": self.utilization,
            "feasible": self.feasible,
            "evidence_ids": list(self.evidence_ids),
            "provenance_ids": list(self.provenance_ids),
        }


def resolve_capacity_constraints(
    capacities: Iterable[CapacityFact],
    requirements: Iterable[CapacityRequirement],
) -> tuple[CapacityConstraint, ...]:
    """Compare canonical capacity with explicit requirements by exact scope."""
    cap_by_key: dict[tuple[str, str], list[CapacityFact]] = {}
    req_by_key: dict[tuple[str, str], list[CapacityRequirement]] = {}
    for fact in capacities:
        cap_by_key.setdefault((fact.resource_id, fact.unit), []).append(fact)
    for req in requirements:
        req_by_key.setdefault((req.resource_id, req.unit), []).append(req)

    results: list[CapacityConstraint] = []
    for key in sorted(set(cap_by_key) | set(req_by_key)):
        cap_facts = cap_by_key.get(key, [])
        req_facts = req_by_key.get(key, [])
        capacity = sum(x.capacity for x in cap_facts)
        required = sum(x.quantity for x in req_facts)
        evidence = sorted({x.evidence_id for x in (*cap_facts, *req_facts) if x.evidence_id})
        provenance = sorted({x.provenance_id for x in (*cap_facts, *req_facts) if x.provenance_id})
        utilization = required / capacity if capacity > 0 else None
        results.append(CapacityConstraint(
            resource_id=key[0], unit=key[1], capacity=capacity, required=required,
            headroom=capacity - required, utilization=utilization,
            feasible=required <= capacity,
            evidence_ids=tuple(evidence), provenance_ids=tuple(provenance),
        ))
    return tuple(results)


def capacity_constraint_to_mapping(result: Iterable[CapacityConstraint]) -> dict[str, Any]:
    return {"contract_version": "S330.1", "constraints": [x.to_mapping() for x in result]}


def capacity_constraint_to_json(result: Iterable[CapacityConstraint]) -> str:
    return json.dumps(capacity_constraint_to_mapping(result), ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
