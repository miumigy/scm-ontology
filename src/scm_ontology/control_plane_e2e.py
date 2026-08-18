"""SCM OS Control Plane E2E (Phase 6, P6-E).

One deterministic user workflow that traverses the full governed control-plane
chain

    State -> Decision -> Simulation/Plan -> Authorization -> Workflow -> Audit

and then composes the P6-A..P6-D control-plane surfaces over the produced
artifacts (cockpit state, decision inbox, simulation/optimization workspace,
and execution workflow workspace). The result is a single immutable,
content-addressed ``ControlPlaneE2EResult``.

P6-E composes the existing governed contracts (demand/supply gap, R5 decision
application S358, governed simulation S363, optimized plan S364, operational
workflow S366). It re-derives no decision and performs no external side
effect.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any

from .decision_inbox import InboxDecision, build_decision_inbox
from .demand_supply_gap import (
    DemandSupplyRecord,
    resolve_demand_supply_gap,
)
from .distribution_application import DistributionObservation
from .governed_simulation import (
    SimulationApplication,
    SimulationStep,
    run_governed_simulation,
)
from .operational_workflow import (
    OperationalStep,
    run_operational_workflow,
)
from .optimized_planning import (
    OptimizedReplenishmentObservation,
    run_optimized_planning,
)
from .replenishment_application import (
    ReplenishmentObservation,
    run_replenishment_application,
)
from .scm_os_cockpit import (
    CockpitFixture,
    build_cockpit_state,
)
from .sim_optim_workspace import (
    workspace_plan,
    workspace_scenario,
    build_workspace_state,
)
from .execution_workspace import (
    launch_execution_workflow,
)


class ControlPlaneE2EError(ValueError):
    """Raised when the control-plane E2E input or invocation is invalid."""


# Stages of the E2E chain, in order.
_STAGES = (
    "state",
    "decision",
    "simulation_plan",
    "authorization",
    "workflow",
    "audit",
)

_SUPPORTED_STAGES = frozenset(_STAGES)


@dataclass(frozen=True)
class ControlPlaneRequest:
    """Explicit operator scope for one deterministic E2E run."""

    context_id: str
    operator_id: str
    authority: str
    observed_at: str

    def __post_init__(self) -> None:
        for name in ("context_id", "operator_id", "authority", "observed_at"):
            if not isinstance(getattr(self, name), str) or not getattr(self, name).strip():
                raise ControlPlaneE2EError(f"{name} must be non-empty")


@dataclass(frozen=True)
class ControlPlaneStage:
    """Deterministic per-stage record of the E2E chain."""

    stage: str
    detail: Any

    def __post_init__(self) -> None:
        if self.stage not in _SUPPORTED_STAGES:
            raise ControlPlaneE2EError(f"unsupported stage: {self.stage}")

    def to_mapping(self) -> dict[str, Any]:
        value: dict[str, Any] = {"stage": self.stage}
        if isinstance(self.detail, dict):
            value.update(self.detail)
        else:
            value["detail"] = self.detail
        return value


@dataclass(frozen=True)
class ControlPlaneE2ESummary:
    """Deterministic aggregate counts across the E2E run."""

    stage_count: int
    actionable_decision: bool
    exception_count: int
    simulation_steps: int
    plan_periods: int
    workflow_steps: int
    governance_audits: int

    def to_mapping(self) -> dict[str, Any]:
        return {
            "stage_count": self.stage_count,
            "actionable_decision": self.actionable_decision,
            "exception_count": self.exception_count,
            "simulation_steps": self.simulation_steps,
            "plan_periods": self.plan_periods,
            "workflow_steps": self.workflow_steps,
            "governance_audits": self.governance_audits,
        }


@dataclass(frozen=True)
class ControlPlaneE2EResult:
    """Immutable, content-addressed outcome of one control-plane E2E run."""

    run_id: str
    request: ControlPlaneRequest
    stages: tuple[ControlPlaneStage, ...]
    # Composed P6-A..P6-D control-plane surfaces.
    surfaces: dict[str, Any]
    summary: ControlPlaneE2ESummary

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "P6E.1",
            "is_control_plane_e2e": True,
            "run_id": self.run_id,
            "request": {
                "context_id": self.request.context_id,
                "operator_id": self.request.operator_id,
                "authority": self.request.authority,
                "observed_at": self.request.observed_at,
            },
            "stages": [stage.to_mapping() for stage in self.stages],
            "surfaces": self.surfaces,
            "summary": self.summary.to_mapping(),
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_mapping(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def run_control_plane_flow(request: ControlPlaneRequest) -> ControlPlaneE2EResult:
    """Run one deterministic control-plane E2E workflow.

    Composes the existing governed contracts end to end, then projects the
    produced artifacts through the P6-A..P6-D control-plane surfaces.
    """
    if not isinstance(request, ControlPlaneRequest):
        raise ControlPlaneE2EError("request must be a ControlPlaneRequest")

    context_id = request.context_id
    operator = request.operator_id
    observed_at = request.observed_at
    authority = request.authority

    # --- Stage 1: State (explicit canonical demand/supply scope) ---
    gaps = resolve_demand_supply_gap(
        (
            DemandSupplyRecord(
                item_id="A-100", quantity=120.0, kind="demand", unit="unit",
                period_start="2026-08-18", period_end="2026-08-18",
                evidence_id="e1", provenance_id="p1",
            ),
            DemandSupplyRecord(
                item_id="A-100", quantity=90.0, kind="supply", unit="unit",
                period_start="2026-08-18", period_end="2026-08-18",
                evidence_id="e2", provenance_id="p2",
            ),
        )
    )

    # --- Stage 2: Decision (replenishment application, S358) ---
    decision = run_replenishment_application(
        ReplenishmentObservation(
            product_id="P-1", location_id="WH-1", on_hand=5.0,
            reorder_point=10.0, reorder_quantity=25.0,
            evidence_ids=("e1",), provenance_ids=("p1",),
        ),
        context_id=context_id, actor_id=operator, authority=authority,
        authorized_at=observed_at, command_id="cmd-e2e",
        dry_ran_at=observed_at,
    )
    governed = decision.governed
    if governed is None:
        raise ControlPlaneE2EError(
            "decision produced no governed result; cannot traverse the chain"
        )

    # --- Stage 3: Simulation / Plan (governed simulation S363 + optimized plan S364) ---
    simulation = run_governed_simulation(
        (
            SimulationStep(
                step_id="s1", application=SimulationApplication.REPLENISHMENT,
                observation=ReplenishmentObservation(
                    product_id="P-1", location_id="WH-1", on_hand=5.0,
                    reorder_point=10.0, reorder_quantity=25.0,
                    evidence_ids=("e1",), provenance_ids=("p1",),
                ),
                command_id="cmd-s1",
            ),
            SimulationStep(
                step_id="s2", application=SimulationApplication.DISTRIBUTION,
                observation=DistributionObservation(
                    shipment_id="S", item_id="I", required_quantity=80.0,
                    capacity=100.0, origin_location_id="WH",
                    destination_location_id="DC",
                    evidence_ids=("e3",), provenance_ids=("p3",),
                ),
                command_id="cmd-s2",
            ),
        ),
        context_id=context_id, actor_id=operator, authority=authority,
        authorized_at=observed_at, dry_ran_at=observed_at,
    )
    optim = run_optimized_planning(
        OptimizedReplenishmentObservation(
            product_id="P-1", location_id="WH-1", demands=(30.0, 40.0, 25.0),
            initial_on_hand=10.0, unit="unit",
            evidence_ids=("e1",), provenance_ids=("p1",),
        ),
        context_id=context_id, actor_id=operator, authority=authority,
        authorized_at=observed_at, command_id_prefix="cmd-op",
        dry_ran_at=observed_at,
    )

    # --- Stage 4: Authorization (already granted by the governed result) ---
    auth = governed.decision.execution_command.decision

    # --- Stage 5: Workflow (operational workflow, S366) ---
    workflow = run_operational_workflow(
        (
            OperationalStep(
                step_id="w1", application="replenishment",
                command_id="cmd-e2e", decision=decision,
            ),
        ),
        workflow_id="wf-e2e", recorded_at=observed_at, actor_id=operator,
    )

    # --- Stage 6: Audit (content-addressed governed audit entries, S354) ---
    audit_steps = [
        {"step_id": s.step_id, "audit_id": s.audit_id, "state": s.state}
        for s in workflow.steps
        if s.audit_id is not None
    ]

    # Compose the P6-A..P6-D control-plane surfaces.
    cockpit = build_cockpit_state(
        CockpitFixture(
            context_id=context_id,
            recorded_at=observed_at,
            actor_id=operator,
            decisions=(decision,),
            gaps=gaps,
            simulation=simulation,
            workflow=workflow,
        )
    )
    inbox = build_decision_inbox(
        (InboxDecision(decision, "dec-e2e"),),
        viewed_at=observed_at, viewer_actor_id=operator,
    )
    workspace = build_workspace_state(
        scenarios=(workspace_scenario(simulation, created_at=observed_at),),
        plans=(workspace_plan(optim, application="replenishment", created_at=observed_at),),
        created_at=observed_at,
        view_actor_id=operator,
    )
    execution = launch_execution_workflow(
        governed_runs=(governed,),
        actor_id=operator,
        recorded_at=observed_at,
        view_actor_id=operator,
        created_at=observed_at,
    )

    stages = (
        ControlPlaneStage(
            "state",
            {"exceptions": [g.to_mapping() for g in gaps]},
        ),
        ControlPlaneStage(
            "decision",
            {"action": decision.action, "governed": governed is not None},
        ),
        ControlPlaneStage(
            "simulation_plan",
            {
                "simulation_steps": len(simulation.steps),
                "plan_periods": len(optim.periods),
            },
        ),
        ControlPlaneStage(
            "authorization",
            {
                "actor_id": auth.actor_id,
                "authority": auth.authority,
                "authorized_at": auth.authorized_at,
            },
        ),
        ControlPlaneStage(
            "workflow",
            {"steps": len(workflow.steps)},
        ),
        ControlPlaneStage("audit", {"entry_count": len(audit_steps)}),
    )

    summary = ControlPlaneE2ESummary(
        stage_count=len(stages),
        actionable_decision=True,
        exception_count=len(gaps),
        simulation_steps=len(simulation.steps),
        plan_periods=len(optim.periods),
        workflow_steps=len(workflow.steps),
        governance_audits=len(audit_steps),
    )

    payload = {
        "context_id": context_id,
        "operator_id": operator,
        "observed_at": observed_at,
        "authority": authority,
        "stages": [stage.to_mapping() for stage in stages],
    }
    run_id = sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()

    return ControlPlaneE2EResult(
        run_id=run_id,
        request=request,
        stages=stages,
        surfaces={
            "cockpit": cockpit.to_mapping(),
            "decision_inbox": inbox.to_mapping(),
            "sim_optim_workspace": workspace.to_mapping(),
            "execution_workspace": execution.to_mapping(),
        },
        summary=summary,
    )
