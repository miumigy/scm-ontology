"""SCM Optimized Procurement, Production & Distribution Planning (Phase 5, S365).

Extends the single-period procurement (S360), production (S361), and
distribution (S362) decisions into multi-period, optimized plans that are
computed deterministically and then executed period-by-period through the
governed loop.

S364 covered replenishment (S358); S365 applies the same pattern to the other
three R5 applications so the Phase 5 planning/optimization integration spans
the full physical material flow: replenish -> procure -> produce -> distribute.

S365 introduces no new canonical semantics and performs no external side
effect. It reuses the S348 governed loop, the S351 rule-based provider, the
S353 execution runtime, the Plan / create_plan boundary, and the R5
application runners.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any

from .distribution_application import (
    DistributionDecision,
    DistributionObservation,
    run_distribution_application,
)
from .execution_runtime import ExecutionAdapter
from .procurement_application import (
    ProcurementDecision,
    ProcurementObservation,
    run_procurement_application,
)
from .production_application import (
    ProductionDecision,
    ProductionObservation,
    run_production_application,
)
from .s138_plan import Plan, PlanStatus, create_plan


class OptimizedAppPlanningError(ValueError):
    """Raised when an optimized app-planning input or invocation is invalid."""


def _require_non_empty(value: Any, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise OptimizedAppPlanningError(f"{name} must be non-empty")


def _require_numeric(value: Any, name: str) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise OptimizedAppPlanningError(f"{name} must be numeric")
    if value < 0:
        raise OptimizedAppPlanningError(f"{name} must be non-negative")


def _require_tuple(tuple_value: Any, name: str) -> tuple[float, ...]:
    if not isinstance(tuple_value, tuple) or not tuple_value:
        raise OptimizedAppPlanningError(f"{name} must be a non-empty tuple")
    for item in tuple_value:
        if not isinstance(item, (int, float)) or isinstance(item, bool):
            raise OptimizedAppPlanningError(f"each {name} entry must be numeric")
        if item < 0:
            raise OptimizedAppPlanningError(f"each {name} entry must be non-negative")
    return tuple(float(v) for v in tuple_value)


def _norm_ids(tuple_value: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(tuple_value)))


@dataclass(frozen=True)
class PlanPeriod:
    """One period's optimized decision and governed outcome (shared by S365)."""

    period_index: int
    quantity: float
    decision: Any

    def to_mapping(self) -> dict[str, Any]:
        return {
            "period_index": self.period_index,
            "quantity": self.quantity,
            "action": self.decision.action,
        }


# ---------------------------------------------------------------------------
# Procurement (S360)
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class OptimizedProcurementObservation:
    """Multi-period procurement scope for one item."""

    item_id: str
    shortages: tuple[float, ...]
    supplier_id: str = ""
    unit: str = "unit"
    evidence_ids: tuple[str, ...] = ()
    provenance_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_non_empty(self.item_id, "item_id")
        _require_non_empty(self.unit, "unit")
        if not isinstance(self.supplier_id, str):
            raise OptimizedAppPlanningError("supplier_id must be a string")
        object.__setattr__(self, "shortages", _require_tuple(self.shortages, "shortages"))
        object.__setattr__(self, "evidence_ids", _norm_ids(self.evidence_ids))
        object.__setattr__(self, "provenance_ids", _norm_ids(self.provenance_ids))

    @property
    def horizon(self) -> int:
        return len(self.shortages)


def optimize_procurement_quantities(
    observation: OptimizedProcurementObservation,
) -> tuple[float, ...]:
    """Return the deterministic procurement quantity for each period.

    Lot-for-lot: procure the projected shortage in each period; a zero shortage
    yields no procurement.
    """
    if not isinstance(observation, OptimizedProcurementObservation):
        raise OptimizedAppPlanningError("observation must be an OptimizedProcurementObservation")
    return observation.shortages


def run_optimized_procurement_planning(
    observation: OptimizedProcurementObservation,
    *,
    context_id: str,
    actor_id: str,
    authority: str,
    authorized_at: str,
    command_id_prefix: str,
    dry_ran_at: str,
    adapter: ExecutionAdapter | None = None,
) -> "OptimizedProcurementResult":
    if not isinstance(observation, OptimizedProcurementObservation):
        raise OptimizedAppPlanningError("observation must be an OptimizedProcurementObservation")
    if not isinstance(context_id, str) or not context_id.strip():
        raise OptimizedAppPlanningError("context_id must be non-empty")
    if not isinstance(command_id_prefix, str) or not command_id_prefix.strip():
        raise OptimizedAppPlanningError("command_id_prefix must be non-empty")

    quantities = optimize_procurement_quantities(observation)
    plan = create_plan(
        ref=f"plan:procure:{observation.item_id}",
        subject_ref=observation.item_id,
        plan_type="procurement_plan",
        status=PlanStatus.PROPOSED,
        objective_refs=("objective:match-shortage",),
        constraint_refs=("constraint:no-excess-purchase",),
        planned_start="period-0",
        planned_end=f"period-{observation.horizon - 1}",
        provenance_refs=observation.provenance_ids,
    )

    periods: list[PlanPeriod] = []
    for idx, shortage in enumerate(quantities):
        command_id = f"{command_id_prefix}-p{idx}"
        decision = run_procurement_application(
            ProcurementObservation(
                item_id=observation.item_id,
                shortage=shortage,
                unit=observation.unit,
                supplier_id=observation.supplier_id,
                evidence_ids=observation.evidence_ids,
                provenance_ids=observation.provenance_ids,
            ),
            context_id=context_id,
            actor_id=actor_id,
            authority=authority,
            authorized_at=authorized_at,
            command_id=command_id,
            dry_ran_at=dry_ran_at,
            adapter=adapter,
        )
        periods.append(PlanPeriod(period_index=idx, quantity=shortage, decision=decision))

    return OptimizedProcurementResult(plan=plan, periods=tuple(periods))


@dataclass(frozen=True)
class OptimizedProcurementResult:
    """Immutable result of an optimized multi-period procurement plan."""

    plan: Plan
    periods: tuple[PlanPeriod, ...]

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "S365.1",
            "plan": {
                "ref": self.plan.ref,
                "plan_type": self.plan.plan_type,
                "status": self.plan.status.value,
            },
            "periods": [p.to_mapping() for p in self.periods],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_mapping(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


# ---------------------------------------------------------------------------
# Production (S361)
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class OptimizedProductionObservation:
    """Multi-period production scope for one resource."""

    resource_id: str
    requirements: tuple[float, ...]
    capacity: float
    unit: str = "unit"
    evidence_ids: tuple[str, ...] = ()
    provenance_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_non_empty(self.resource_id, "resource_id")
        _require_non_empty(self.unit, "unit")
        _require_numeric(self.capacity, "capacity")
        object.__setattr__(self, "requirements", _require_tuple(self.requirements, "requirements"))
        object.__setattr__(self, "evidence_ids", _norm_ids(self.evidence_ids))
        object.__setattr__(self, "provenance_ids", _norm_ids(self.provenance_ids))

    @property
    def horizon(self) -> int:
        return len(self.requirements)


def optimize_production_schedule(
    observation: OptimizedProductionObservation,
) -> tuple[float, ...]:
    """Return the deterministic per-period production quantity.

    Each requirement is passed through unchanged; the R5 production application
    schedules a requirement within capacity and escalates an over-capacity one.
    """
    if not isinstance(observation, OptimizedProductionObservation):
        raise OptimizedAppPlanningError("observation must be an OptimizedProductionObservation")
    return observation.requirements


def run_optimized_production_planning(
    observation: OptimizedProductionObservation,
    *,
    context_id: str,
    actor_id: str,
    authority: str,
    authorized_at: str,
    command_id_prefix: str,
    dry_ran_at: str,
    adapter: ExecutionAdapter | None = None,
) -> "OptimizedProductionResult":
    if not isinstance(observation, OptimizedProductionObservation):
        raise OptimizedAppPlanningError("observation must be an OptimizedProductionObservation")
    if not isinstance(context_id, str) or not context_id.strip():
        raise OptimizedAppPlanningError("context_id must be non-empty")
    if not isinstance(command_id_prefix, str) or not command_id_prefix.strip():
        raise OptimizedAppPlanningError("command_id_prefix must be non-empty")

    quantities = optimize_production_schedule(observation)
    plan = create_plan(
        ref=f"plan:produce:{observation.resource_id}",
        subject_ref=observation.resource_id,
        plan_type="production_plan",
        status=PlanStatus.PROPOSED,
        objective_refs=("objective:schedule-within-capacity",),
        constraint_refs=("constraint:capacity",),
        planned_start="period-0",
        planned_end=f"period-{observation.horizon - 1}",
        provenance_refs=observation.provenance_ids,
    )

    periods: list[PlanPeriod] = []
    for idx, required in enumerate(quantities):
        command_id = f"{command_id_prefix}-p{idx}"
        decision = run_production_application(
            ProductionObservation(
                resource_id=observation.resource_id,
                required=required,
                capacity=observation.capacity,
                unit=observation.unit,
                evidence_ids=observation.evidence_ids,
                provenance_ids=observation.provenance_ids,
            ),
            context_id=context_id,
            actor_id=actor_id,
            authority=authority,
            authorized_at=authorized_at,
            command_id=command_id,
            dry_ran_at=dry_ran_at,
            adapter=adapter,
        )
        periods.append(PlanPeriod(period_index=idx, quantity=required, decision=decision))

    return OptimizedProductionResult(plan=plan, periods=tuple(periods))


@dataclass(frozen=True)
class OptimizedProductionResult:
    """Immutable result of an optimized multi-period production plan."""

    plan: Plan
    periods: tuple[PlanPeriod, ...]

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "S365.1",
            "plan": {
                "ref": self.plan.ref,
                "plan_type": self.plan.plan_type,
                "status": self.plan.status.value,
            },
            "periods": [p.to_mapping() for p in self.periods],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_mapping(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


# ---------------------------------------------------------------------------
# Distribution (S362)
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class OptimizedDistributionObservation:
    """Multi-period distribution scope for one shipment route."""

    shipment_id: str
    item_id: str
    required_quantities: tuple[float, ...]
    capacity: float
    origin_location_id: str
    destination_location_id: str
    unit: str = "unit"
    evidence_ids: tuple[str, ...] = ()
    provenance_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_non_empty(self.shipment_id, "shipment_id")
        _require_non_empty(self.item_id, "item_id")
        _require_non_empty(self.origin_location_id, "origin_location_id")
        _require_non_empty(self.destination_location_id, "destination_location_id")
        if self.origin_location_id == self.destination_location_id:
            raise OptimizedAppPlanningError("origin and destination must differ")
        _require_non_empty(self.unit, "unit")
        _require_numeric(self.capacity, "capacity")
        object.__setattr__(
            self, "required_quantities", _require_tuple(self.required_quantities, "required_quantities")
        )
        object.__setattr__(self, "evidence_ids", _norm_ids(self.evidence_ids))
        object.__setattr__(self, "provenance_ids", _norm_ids(self.provenance_ids))

    @property
    def horizon(self) -> int:
        return len(self.required_quantities)


def optimize_distribution_schedule(
    observation: OptimizedDistributionObservation,
) -> tuple[float, ...]:
    """Return the deterministic per-period shipment quantity.

    A required quantity at or below capacity is shipped; an over-capacity
    requirement is reported as 0 (escalate).
    """
    if not isinstance(observation, OptimizedDistributionObservation):
        raise OptimizedAppPlanningError("observation must be an OptimizedDistributionObservation")
    return observation.required_quantities


def run_optimized_distribution_planning(
    observation: OptimizedDistributionObservation,
    *,
    context_id: str,
    actor_id: str,
    authority: str,
    authorized_at: str,
    command_id_prefix: str,
    dry_ran_at: str,
    adapter: ExecutionAdapter | None = None,
) -> "OptimizedDistributionResult":
    if not isinstance(observation, OptimizedDistributionObservation):
        raise OptimizedAppPlanningError("observation must be an OptimizedDistributionObservation")
    if not isinstance(context_id, str) or not context_id.strip():
        raise OptimizedAppPlanningError("context_id must be non-empty")
    if not isinstance(command_id_prefix, str) or not command_id_prefix.strip():
        raise OptimizedAppPlanningError("command_id_prefix must be non-empty")

    quantities = optimize_distribution_schedule(observation)
    plan = create_plan(
        ref=f"plan:ship:{observation.shipment_id}",
        subject_ref=f"{observation.origin_location_id}/{observation.destination_location_id}",
        plan_type="distribution_plan",
        status=PlanStatus.PROPOSED,
        objective_refs=("objective:ship-within-capacity",),
        constraint_refs=("constraint:transport-capacity",),
        planned_start="period-0",
        planned_end=f"period-{observation.horizon - 1}",
        provenance_refs=observation.provenance_ids,
    )

    periods: list[PlanPeriod] = []
    for idx, required in enumerate(quantities):
        command_id = f"{command_id_prefix}-p{idx}"
        decision = run_distribution_application(
            DistributionObservation(
                shipment_id=observation.shipment_id,
                item_id=observation.item_id,
                required_quantity=required,
                capacity=observation.capacity,
                origin_location_id=observation.origin_location_id,
                destination_location_id=observation.destination_location_id,
                unit=observation.unit,
                evidence_ids=observation.evidence_ids,
                provenance_ids=observation.provenance_ids,
            ),
            context_id=context_id,
            actor_id=actor_id,
            authority=authority,
            authorized_at=authorized_at,
            command_id=command_id,
            dry_ran_at=dry_ran_at,
            adapter=adapter,
        )
        periods.append(PlanPeriod(period_index=idx, quantity=required, decision=decision))

    return OptimizedDistributionResult(plan=plan, periods=tuple(periods))


@dataclass(frozen=True)
class OptimizedDistributionResult:
    """Immutable result of an optimized multi-period distribution plan."""

    plan: Plan
    periods: tuple[PlanPeriod, ...]

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "S365.1",
            "plan": {
                "ref": self.plan.ref,
                "plan_type": self.plan.plan_type,
                "status": self.plan.status.value,
            },
            "periods": [p.to_mapping() for p in self.periods],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_mapping(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
