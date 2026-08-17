"""SCM Optimized Replenishment Plan Application (Phase 5, S364).

Extends the single-period replenishment decision (S358) into a multi-period,
cost-aware replenishment plan that is optimized deterministically and then
executed period-by-period through the governed loop.

It composes existing boundaries without introducing new canonical semantics:
the `Plan` / `create_plan` boundary for the plan artifact, the planning
boundary concept surfaced as explicit plan metadata (objective/constraint
refs), and the S348 governed loop + S358 replenishment application for each
period's execution. S364 performs no external side effect and never mutates
Canonical Truth.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any

from .execution_runtime import ExecutionAdapter
from .replenishment_application import (
    ReplenishmentDecision,
    ReplenishmentObservation,
    run_replenishment_application,
)
from .s138_plan import Plan, PlanStatus, create_plan


class OptimizedPlanningError(ValueError):
    """Raised when an optimized planning input or invocation is invalid."""


@dataclass(frozen=True)
class OptimizedReplenishmentObservation:
    """Multi-period replenishment scope for one product/location.

    ``demands`` is an ordered tuple of non-negative quantities, one per period.
    The optimizer computes a deterministic replenishment quantity for each
    period so that inventory covers demand without stockout.
    """

    product_id: str
    location_id: str
    demands: tuple[float, ...]
    initial_on_hand: float = 0.0
    reorder_point: float = 0.0
    unit: str = "unit"
    evidence_ids: tuple[str, ...] = ()
    provenance_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.product_id, str) or not self.product_id.strip():
            raise OptimizedPlanningError("product_id must be non-empty")
        if not isinstance(self.location_id, str) or not self.location_id.strip():
            raise OptimizedPlanningError("location_id must be non-empty")
        if not isinstance(self.unit, str) or not self.unit.strip():
            raise OptimizedPlanningError("unit must be non-empty")
        for name in ("initial_on_hand", "reorder_point"):
            value = getattr(self, name)
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise OptimizedPlanningError(f"{name} must be numeric")
            if value < 0:
                raise OptimizedPlanningError(f"{name} must be non-negative")
        if not isinstance(self.demands, tuple) or not self.demands:
            raise OptimizedPlanningError("demands must be a non-empty tuple")
        for d in self.demands:
            if not isinstance(d, (int, float)) or isinstance(d, bool):
                raise OptimizedPlanningError("each demand must be numeric")
            if d < 0:
                raise OptimizedPlanningError("each demand must be non-negative")
        object.__setattr__(self, "demands", tuple(float(d) for d in self.demands))
        object.__setattr__(self, "evidence_ids", tuple(sorted(set(self.evidence_ids))))
        object.__setattr__(self, "provenance_ids", tuple(sorted(set(self.provenance_ids))))

    @property
    def horizon(self) -> int:
        return len(self.demands)


def optimize_replenishment_quantities(
    observation: OptimizedReplenishmentObservation,
) -> tuple[float, ...]:
    """Return the deterministic replenishment quantity for each period.

    Lot-for-lot policy: replenish only the projected shortfall in each period,
    carrying inventory forward. This minimizes total holding cost while
    avoiding stockouts over the horizon.
    """
    if not isinstance(observation, OptimizedReplenishmentObservation):
        raise OptimizedPlanningError("observation must be an OptimizedReplenishmentObservation")
    on_hand = observation.initial_on_hand
    quantities: list[float] = []
    for demand in observation.demands:
        if on_hand < demand:
            shortfall = demand - on_hand
            qty = shortfall
            if observation.reorder_point > 0 and on_hand < observation.reorder_point:
                qty = shortfall + observation.reorder_point
            quantities.append(qty)
            on_hand = on_hand + qty - demand
        else:
            quantities.append(0.0)
            on_hand = on_hand - demand
    return tuple(quantities)


def _replenishment_observation(
    observation: OptimizedReplenishmentObservation,
    quantity: float,
) -> ReplenishmentObservation:
    """Project one optimized period into an S358 replenishment observation.

    A zero quantity is represented as on-hand above the effective reorder point
    (no reorder). A positive quantity is represented as on-hand below the point
    (reorder), with the optimized quantity as the reorder quantity. An
    effective reorder point of at least 1 is used so a positive quantity always
    triggers a reorder through the S358 application.
    """
    effective_point = observation.reorder_point if observation.reorder_point > 0 else 1.0
    if quantity <= 0:
        return ReplenishmentObservation(
            product_id=observation.product_id,
            location_id=observation.location_id,
            on_hand=effective_point + 1.0,
            reorder_point=effective_point,
            reorder_quantity=0.0,
            unit=observation.unit,
            evidence_ids=observation.evidence_ids,
            provenance_ids=observation.provenance_ids,
        )
    return ReplenishmentObservation(
        product_id=observation.product_id,
        location_id=observation.location_id,
        on_hand=0.0,
        reorder_point=effective_point,
        reorder_quantity=quantity,
        unit=observation.unit,
        evidence_ids=observation.evidence_ids,
        provenance_ids=observation.provenance_ids,
    )


@dataclass(frozen=True)
class PlanPeriodDecision:
    """One period's optimized replenishment decision and governed outcome."""

    period_index: int
    quantity: float
    decision: ReplenishmentDecision

    def to_mapping(self) -> dict[str, Any]:
        return {
            "period_index": self.period_index,
            "quantity": self.quantity,
            "action": self.decision.action,
        }


@dataclass(frozen=True)
class OptimizedPlanningResult:
    """Immutable result of an optimized multi-period replenishment plan."""

    plan: Plan
    periods: tuple[PlanPeriodDecision, ...]

    @property
    def total_replenishment(self) -> float:
        return round(sum(p.quantity for p in self.periods), 6)

    @property
    def plan_ref(self) -> str:
        return self.plan.ref

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "S364.1",
            "plan": {
                "ref": self.plan.ref,
                "plan_type": self.plan.plan_type,
                "status": self.plan.status.value,
                "objective_refs": list(self.plan.objective_refs),
                "constraint_refs": list(self.plan.constraint_refs),
            },
            "periods": [p.to_mapping() for p in self.periods],
            "total_replenishment": self.total_replenishment,
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def run_optimized_planning(
    observation: OptimizedReplenishmentObservation,
    *,
    context_id: str,
    actor_id: str,
    authority: str,
    authorized_at: str,
    command_id_prefix: str,
    dry_ran_at: str,
    adapter: ExecutionAdapter | None = None,
) -> OptimizedPlanningResult:
    """Optimize a multi-period replenishment plan and run it through the loop."""
    if not isinstance(observation, OptimizedReplenishmentObservation):
        raise OptimizedPlanningError("observation must be an OptimizedReplenishmentObservation")
    if not isinstance(context_id, str) or not context_id.strip():
        raise OptimizedPlanningError("context_id must be non-empty")
    if not isinstance(command_id_prefix, str) or not command_id_prefix.strip():
        raise OptimizedPlanningError("command_id_prefix must be non-empty")

    quantities = optimize_replenishment_quantities(observation)

    plan = create_plan(
        ref=f"plan:{observation.product_id}:{observation.location_id}",
        subject_ref=f"{observation.product_id}/{observation.location_id}",
        plan_type="replenishment_plan",
        status=PlanStatus.PROPOSED,
        objective_refs=("objective:minimize-holding-cost",),
        constraint_refs=("constraint:no-stockout",),
        planned_start="period-0",
        planned_end=f"period-{observation.horizon - 1}",
        provenance_refs=observation.provenance_ids,
    )

    periods: list[PlanPeriodDecision] = []
    for idx, quantity in enumerate(quantities):
        command_id = f"{command_id_prefix}-p{idx}"
        period_obs = _replenishment_observation(observation, quantity)
        decision = run_replenishment_application(
            period_obs,
            context_id=context_id,
            actor_id=actor_id,
            authority=authority,
            authorized_at=authorized_at,
            command_id=command_id,
            dry_ran_at=dry_ran_at,
            adapter=adapter,
        )
        periods.append(PlanPeriodDecision(period_index=idx, quantity=quantity, decision=decision))

    return OptimizedPlanningResult(plan=plan, periods=tuple(periods))
