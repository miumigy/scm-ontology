"""SCM OS Simulation / Optimization Workspace (Phase 6, P6-C).

A control-plane workspace for launching and inspecting **deterministic
scenarios and plans** from the same surface. P6-C composes the existing
governed contracts:

  - governed simulation (S363) -> scenarios;
  - optimized replenishment planning (S364) and optimized
    procurement/production/distribution planning (S365) -> plans.

It projects each launched artifact into an immutable, deterministic, JSON-safe
``WorkspaceScenario`` / ``WorkspacePlan`` and folds them into a content-addressed
``WorkspaceState`` with a workspace summary.

P6-C never re-derives or mutates a scenario/plan and performs no external side
effect. Launching composes the existing launchers; inspection is read-only.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Iterable

from .execution_runtime import ExecutionAdapter
from .governed_simulation import (
    GovernedSimulationResult,
    SimulationApplication,
    SimulationStep,
    run_governed_simulation,
)
from .optimized_app_planning import (
    OptimizedDistributionObservation,
    OptimizedDistributionResult,
    OptimizedProcurementObservation,
    OptimizedProcurementResult,
    OptimizedProductionObservation,
    OptimizedProductionResult,
    run_optimized_distribution_planning,
    run_optimized_procurement_planning,
    run_optimized_production_planning,
)
from .optimized_planning import (
    OptimizedPlanningResult,
    OptimizedReplenishmentObservation,
    run_optimized_planning,
)


class WorkspaceError(ValueError):
    """Raised when a workspace input or invocation is invalid."""


# Plan result families accepted by the workspace projection.
_PLAN_RESULTS = (
    OptimizedPlanningResult,
    OptimizedProcurementResult,
    OptimizedProductionResult,
    OptimizedDistributionResult,
)

_SCENARIO_TYPE = GovernedSimulationResult


@dataclass(frozen=True)
class WorkspaceScenario:
    """Immutable inspectable projection of one launched scenario."""

    scenario_id: str
    context_id: str
    created_at: str
    step_count: int
    actionable_steps: int
    no_action_steps: int
    artifact: GovernedSimulationResult

    def __post_init__(self) -> None:
        if not isinstance(self.scenario_id, str) or not self.scenario_id.strip():
            raise WorkspaceError("scenario_id must be non-empty")
        if not isinstance(self.context_id, str) or not self.context_id.strip():
            raise WorkspaceError("context_id must be non-empty")
        if not isinstance(self.created_at, str) or not self.created_at.strip():
            raise WorkspaceError("created_at must be non-empty")
        if not isinstance(self.artifact, _SCENARIO_TYPE):
            raise WorkspaceError(
                "artifact must be a GovernedSimulationResult"
            )

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P6C.1",
            "kind": "scenario",
            "scenario_id": self.scenario_id,
            "context_id": self.context_id,
            "created_at": self.created_at,
            "step_count": self.step_count,
            "actionable_steps": self.actionable_steps,
            "no_action_steps": self.no_action_steps,
        }


@dataclass(frozen=True)
class WorkspacePlan:
    """Immutable inspectable projection of one launched plan."""

    plan_ref: str
    plan_type: str
    status: str
    application: str
    created_at: str
    contract_version: str
    period_count: int
    total_quantity: float
    artifact: Any

    def __post_init__(self) -> None:
        if not isinstance(self.plan_ref, str) or not self.plan_ref.strip():
            raise WorkspaceError("plan_ref must be non-empty")
        if not isinstance(self.plan_type, str) or not self.plan_type.strip():
            raise WorkspaceError("plan_type must be non-empty")
        if not isinstance(self.application, str) or not self.application.strip():
            raise WorkspaceError("application must be non-empty")
        if not isinstance(self.created_at, str) or not self.created_at.strip():
            raise WorkspaceError("created_at must be non-empty")

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P6C.1",
            "kind": "plan",
            "plan_ref": self.plan_ref,
            "plan_type": self.plan_type,
            "status": self.status,
            "application": self.application,
            "created_at": self.created_at,
            "source_contract_version": self.contract_version,
            "period_count": self.period_count,
            "total_quantity": self.total_quantity,
        }


@dataclass(frozen=True)
class WorkspaceSummary:
    """Deterministic aggregate counts across the workspace."""

    scenario_count: int
    plan_count: int
    total_steps: int
    total_periods: int

    def to_mapping(self) -> dict[str, Any]:
        return {
            "scenario_count": self.scenario_count,
            "plan_count": self.plan_count,
            "total_steps": self.total_steps,
            "total_periods": self.total_periods,
        }


@dataclass(frozen=True)
class WorkspaceState:
    """Immutable, content-addressed workspace snapshot."""

    workspace_id: str
    created_at: str
    view_actor_id: str
    scenarios: tuple[WorkspaceScenario, ...]
    plans: tuple[WorkspacePlan, ...]
    summary: WorkspaceSummary

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P6C.1",
            "is_workspace": True,
            "workspace_id": self.workspace_id,
            "created_at": self.created_at,
            "view_actor_id": self.view_actor_id,
            "summary": self.summary.to_mapping(),
            "scenarios": [s.to_mapping() for s in self.scenarios],
            "plans": [p.to_mapping() for p in self.plans],
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def _application_for_plan(result: Any) -> str:
    if isinstance(result, OptimizedPlanningResult):
        return "replenishment"
    if isinstance(result, OptimizedProcurementResult):
        return "procurement"
    if isinstance(result, OptimizedProductionResult):
        return "production"
    if isinstance(result, OptimizedDistributionResult):
        return "distribution"
    raise WorkspaceError(
        f"unsupported plan artifact: {type(result).__name__}"
    )


def _plan_projection(result: Any, application: str | None, created_at: str) -> WorkspacePlan:
    plan = result.plan
    total = round(sum(float(getattr(p, "quantity", 0.0)) for p in result.periods), 6)
    return WorkspacePlan(
        plan_ref=getattr(plan, "ref", ""),
        plan_type=getattr(plan, "plan_type", ""),
        status=getattr(plan, "status", "proposed").value
        if hasattr(getattr(plan, "status", None), "value")
        else str(getattr(plan, "status", "")),
        application=application or _application_for_plan(result),
        created_at=created_at,
        contract_version=result.to_mapping().get("contract_version", ""),
        period_count=len(result.periods),
        total_quantity=total,
        artifact=result,
    )


def _scenario_projection(
    result: GovernedSimulationResult, scenario_id: str | None, created_at: str
) -> WorkspaceScenario:
    if not isinstance(result, _SCENARIO_TYPE):
        raise WorkspaceError("result must be a GovernedSimulationResult")
    actionable = 0
    no_action = 0
    for step in result.steps:
        governed = getattr(step.decision, "governed", None)
        if governed is None:
            no_action += 1
        else:
            actionable += 1
    return WorkspaceScenario(
        scenario_id=scenario_id or result.simulation_run_id,
        context_id=result.context_id,
        created_at=created_at,
        step_count=len(result.steps),
        actionable_steps=actionable,
        no_action_steps=no_action,
        artifact=result,
    )


def workspace_scenario(
    result: GovernedSimulationResult,
    *,
    scenario_id: str | None = None,
    created_at: str,
) -> WorkspaceScenario:
    """Project an already-produced simulation into an inspectable scenario."""
    return _scenario_projection(result, scenario_id, created_at)


def workspace_plan(
    result: Any,
    *,
    application: str | None = None,
    created_at: str,
) -> WorkspacePlan:
    """Project an already-produced optimized plan into an inspectable plan."""
    if not isinstance(result, _PLAN_RESULTS):
        raise WorkspaceError(
            f"unsupported plan artifact: {type(result).__name__}"
        )
    return _plan_projection(result, application, created_at)


# ---------------------------------------------------------------------------
# Launch helpers (compose the existing governed launchers)
# ---------------------------------------------------------------------------


def launch_simulation(
    steps: Iterable[SimulationStep],
    *,
    context_id: str,
    actor_id: str,
    authority: str,
    authorized_at: str,
    dry_ran_at: str,
    created_at: str,
    adapter: ExecutionAdapter | None = None,
) -> WorkspaceScenario:
    """Launch a governed simulation scenario (composes S363)."""
    result = run_governed_simulation(
        steps,
        context_id=context_id,
        actor_id=actor_id,
        authority=authority,
        authorized_at=authorized_at,
        dry_ran_at=dry_ran_at,
        adapter=adapter,
    )
    return _scenario_projection(result, None, created_at)


def launch_replenishment_plan(
    observation: OptimizedReplenishmentObservation,
    *,
    context_id: str,
    actor_id: str,
    authority: str,
    authorized_at: str,
    command_id_prefix: str,
    dry_ran_at: str,
    created_at: str,
    adapter: ExecutionAdapter | None = None,
) -> WorkspacePlan:
    """Launch an optimized replenishment plan (composes S364)."""
    result = run_optimized_planning(
        observation,
        context_id=context_id,
        actor_id=actor_id,
        authority=authority,
        authorized_at=authorized_at,
        command_id_prefix=command_id_prefix,
        dry_ran_at=dry_ran_at,
        adapter=adapter,
    )
    return _plan_projection(result, "replenishment", created_at)


def launch_procurement_plan(
    observation: OptimizedProcurementObservation,
    *,
    context_id: str,
    actor_id: str,
    authority: str,
    authorized_at: str,
    command_id_prefix: str,
    dry_ran_at: str,
    created_at: str,
    adapter: ExecutionAdapter | None = None,
) -> WorkspacePlan:
    """Launch an optimized procurement plan (composes S365)."""
    result = run_optimized_procurement_planning(
        observation,
        context_id=context_id,
        actor_id=actor_id,
        authority=authority,
        authorized_at=authorized_at,
        command_id_prefix=command_id_prefix,
        dry_ran_at=dry_ran_at,
        adapter=adapter,
    )
    return _plan_projection(result, "procurement", created_at)


def launch_production_plan(
    observation: OptimizedProductionObservation,
    *,
    context_id: str,
    actor_id: str,
    authority: str,
    authorized_at: str,
    command_id_prefix: str,
    dry_ran_at: str,
    created_at: str,
    adapter: ExecutionAdapter | None = None,
) -> WorkspacePlan:
    """Launch an optimized production plan (composes S365)."""
    result = run_optimized_production_planning(
        observation,
        context_id=context_id,
        actor_id=actor_id,
        authority=authority,
        authorized_at=authorized_at,
        command_id_prefix=command_id_prefix,
        dry_ran_at=dry_ran_at,
        adapter=adapter,
    )
    return _plan_projection(result, "production", created_at)


def launch_distribution_plan(
    observation: OptimizedDistributionObservation,
    *,
    context_id: str,
    actor_id: str,
    authority: str,
    authorized_at: str,
    command_id_prefix: str,
    dry_ran_at: str,
    created_at: str,
    adapter: ExecutionAdapter | None = None,
) -> WorkspacePlan:
    """Launch an optimized distribution plan (composes S365)."""
    result = run_optimized_distribution_planning(
        observation,
        context_id=context_id,
        actor_id=actor_id,
        authority=authority,
        authorized_at=authorized_at,
        command_id_prefix=command_id_prefix,
        dry_ran_at=dry_ran_at,
        adapter=adapter,
    )
    return _plan_projection(result, "distribution", created_at)


# ---------------------------------------------------------------------------
# Workspace state assembly
# ---------------------------------------------------------------------------


def build_workspace_state(
    *,
    scenarios: Iterable[WorkspaceScenario],
    plans: Iterable[WorkspacePlan],
    created_at: str,
    view_actor_id: str,
) -> WorkspaceState:
    """Fold launched scenarios/plans into an immutable workspace snapshot."""
    if not isinstance(created_at, str) or not created_at.strip():
        raise WorkspaceError("created_at must be non-empty")
    if not isinstance(view_actor_id, str) or not view_actor_id.strip():
        raise WorkspaceError("view_actor_id must be non-empty")

    try:
        scenarios_tuple = tuple(scenarios)
        plans_tuple = tuple(plans)
    except TypeError as exc:
        raise WorkspaceError("scenarios and plans must be iterable") from exc

    if not scenarios_tuple and not plans_tuple:
        raise WorkspaceError("workspace must contain at least one scenario or plan")

    for scenario in scenarios_tuple:
        if not isinstance(scenario, WorkspaceScenario):
            raise WorkspaceError("every scenario must be a WorkspaceScenario")
    for plan in plans_tuple:
        if not isinstance(plan, WorkspacePlan):
            raise WorkspaceError("every plan must be a WorkspacePlan")

    scenario_ids = [s.scenario_id for s in scenarios_tuple]
    if len(scenario_ids) != len(set(scenario_ids)):
        raise WorkspaceError("scenario ids must be unique within the workspace")
    plan_refs = [p.plan_ref for p in plans_tuple]
    if len(plan_refs) != len(set(plan_refs)):
        raise WorkspaceError("plan refs must be unique within the workspace")

    summary = WorkspaceSummary(
        scenario_count=len(scenarios_tuple),
        plan_count=len(plans_tuple),
        total_steps=sum(s.step_count for s in scenarios_tuple),
        total_periods=sum(p.period_count for p in plans_tuple),
    )

    payload = {
        "created_at": created_at,
        "view_actor_id": view_actor_id,
        "scenarios": [s.to_mapping() for s in scenarios_tuple],
        "plans": [p.to_mapping() for p in plans_tuple],
    }
    workspace_id = sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return WorkspaceState(
        workspace_id=workspace_id,
        created_at=created_at,
        view_actor_id=view_actor_id,
        scenarios=scenarios_tuple,
        plans=plans_tuple,
        summary=summary,
    )


def launch_reference_workspace(
    *,
    created_at: str = "2026-08-18T13:00:00Z",
    view_actor_id: str = "planner-1",
) -> WorkspaceState:
    """Deterministic reference path: launch one scenario + the four plans."""
    from .distribution_application import DistributionObservation
    from .replenishment_application import ReplenishmentObservation

    context_id = "ctx-workspace"
    actor_id = view_actor_id
    authority = "supply-chain-manager"
    authorized_at = created_at
    dry_ran_at = created_at

    scenario = launch_simulation(
        (
            SimulationStep(
                step_id="sim-1", application=SimulationApplication.REPLENISHMENT,
                observation=ReplenishmentObservation(
                    product_id="P-1", location_id="WH-1", on_hand=5.0,
                    reorder_point=10.0, reorder_quantity=25.0,
                    evidence_ids=("e1",), provenance_ids=("p1",),
                ),
                command_id="cmd-sr",
            ),
            SimulationStep(
                step_id="sim-2", application=SimulationApplication.DISTRIBUTION,
                observation=DistributionObservation(
                    shipment_id="S", item_id="I", required_quantity=80.0,
                    capacity=100.0, origin_location_id="WH",
                    destination_location_id="DC",
                    evidence_ids=("e3",), provenance_ids=("p3",),
                ),
                command_id="cmd-sd",
            ),
        ),
        context_id=context_id, actor_id=actor_id, authority=authority,
        authorized_at=authorized_at, dry_ran_at=dry_ran_at, created_at=created_at,
    )

    plan_r = launch_replenishment_plan(
        OptimizedReplenishmentObservation(
            product_id="P-1", location_id="WH-1", demands=(30.0, 40.0, 25.0),
            initial_on_hand=10.0, unit="unit",
            evidence_ids=("e1",), provenance_ids=("p1",),
        ),
        context_id=context_id, actor_id=actor_id, authority=authority,
        authorized_at=authorized_at, command_id_prefix="cmd-pr",
        dry_ran_at=dry_ran_at, created_at=created_at,
    )

    plan_u = launch_procurement_plan(
        OptimizedProcurementObservation(
            item_id="ITEM-1", shortages=(20.0, 15.0, 0.0),
            supplier_id="SUP-1", unit="unit",
            evidence_ids=("e2",), provenance_ids=("p2",),
        ),
        context_id=context_id, actor_id=actor_id, authority=authority,
        authorized_at=authorized_at, command_id_prefix="cmd-pp",
        dry_ran_at=dry_ran_at, created_at=created_at,
    )

    plan_p = launch_production_plan(
        OptimizedProductionObservation(
            resource_id="LINE-1", requirements=(80.0, 60.0, 70.0),
            capacity=100.0, unit="unit",
            evidence_ids=("e3",), provenance_ids=("p3",),
        ),
        context_id=context_id, actor_id=actor_id, authority=authority,
        authorized_at=authorized_at, command_id_prefix="cmd-pd",
        dry_ran_at=dry_ran_at, created_at=created_at,
    )

    plan_d = launch_distribution_plan(
        OptimizedDistributionObservation(
            shipment_id="S", item_id="I", required_quantities=(60.0, 50.0, 40.0),
            capacity=80.0, origin_location_id="WH", destination_location_id="DC",
            unit="unit", evidence_ids=("e4",), provenance_ids=("p4",),
        ),
        context_id=context_id, actor_id=actor_id, authority=authority,
        authorized_at=authorized_at, command_id_prefix="cmd-ds",
        dry_ran_at=dry_ran_at, created_at=created_at,
    )

    return build_workspace_state(
        scenarios=(scenario,),
        plans=(plan_r, plan_u, plan_p, plan_d),
        created_at=created_at,
        view_actor_id=view_actor_id,
    )
