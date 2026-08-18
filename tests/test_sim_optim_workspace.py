from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.distribution_application import DistributionObservation
from scm_ontology.governed_simulation import (
    SimulationApplication,
    SimulationStep,
)
from scm_ontology.optimized_app_planning import (
    OptimizedDistributionObservation,
    OptimizedProcurementObservation,
    OptimizedProductionObservation,
)
from scm_ontology.optimized_planning import OptimizedReplenishmentObservation
from scm_ontology.replenishment_application import ReplenishmentObservation
from scm_ontology.sim_optim_workspace import (
    WorkspaceError,
    WorkspacePlan,
    WorkspaceScenario,
    WorkspaceState,
    build_workspace_state,
    launch_distribution_plan,
    launch_procurement_plan,
    launch_production_plan,
    launch_reference_workspace,
    launch_replenishment_plan,
    launch_simulation,
    workspace_plan,
)


def ws_args(**overrides):
    args = dict(
        context_id="ctx-ws",
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-18T13:00:00Z",
        dry_ran_at="2026-08-18T13:00:01Z",
        created_at="2026-08-18T13:00:02Z",
    )
    args.update(overrides)
    return args


def scenario(**overrides):
    args = ws_args()
    args.update(overrides)
    sc = launch_simulation(
        (
            SimulationStep(
                step_id="a", application=SimulationApplication.REPLENISHMENT,
                observation=ReplenishmentObservation(
                    product_id="P-1", location_id="WH-1", on_hand=5.0,
                    reorder_point=10.0, reorder_quantity=25.0,
                    evidence_ids=("e1",), provenance_ids=("p1",),
                ),
                command_id="cmd-a",
            ),
            SimulationStep(
                step_id="b", application=SimulationApplication.DISTRIBUTION,
                observation=DistributionObservation(
                    shipment_id="S", item_id="I", required_quantity=120.0,
                    capacity=100.0, origin_location_id="WH",
                    destination_location_id="DC",
                    evidence_ids=("e2",), provenance_ids=("p2",),
                ),
                command_id="cmd-b",
            ),
        ),
        **args,
    )
    return sc


def plan(**overrides):
    args = ws_args()
    args.update(overrides)
    return launch_replenishment_plan(
        OptimizedReplenishmentObservation(
            product_id="P-1", location_id="WH-1", demands=(30.0, 40.0, 25.0),
            initial_on_hand=10.0, unit="unit",
            evidence_ids=("e1",), provenance_ids=("p1",),
        ),
        command_id_prefix="cmd-pr",
        **args,
    )


def workspaces(**overrides):
    args = dict(created_at="2026-08-18T13:00:02Z", view_actor_id="operator-1")
    args.update(overrides)
    return build_workspace_state(scenarios=(scenario(),), plans=(plan(),), **args)


def test_workspace_versioned_and_labeled():
    ws = workspaces()
    m = ws.to_mapping()
    assert m["contract_version"] == "P6C.1"
    assert m["is_workspace"] is True
    assert m["view_actor_id"] == "operator-1"


def test_scenario_projection_counts():
    sc = scenario()
    m = sc.to_mapping()
    assert m["kind"] == "scenario"
    assert m["context_id"] == "ctx-ws"
    assert m["step_count"] == 2
    assert m["actionable_steps"] == 1
    assert m["no_action_steps"] == 1


def test_plan_projection_counts():
    p = plan()
    m = p.to_mapping()
    assert m["kind"] == "plan"
    assert m["application"] == "replenishment"
    assert m["plan_type"] == "replenishment_plan"
    assert m["period_count"] == 3
    assert m["total_quantity"] == pytest.approx(85.0)
    assert m["source_contract_version"] == "S364.1"


def test_workspace_summary():
    ws = workspaces()
    s = ws.to_mapping()["summary"]
    assert s["scenario_count"] == 1
    assert s["plan_count"] == 1
    assert s["total_steps"] == 2
    assert s["total_periods"] == 3


def test_reference_workspace_spans_all_applications():
    ws = launch_reference_workspace()
    m = ws.to_mapping()
    assert m["summary"]["scenario_count"] == 1
    assert m["summary"]["plan_count"] == 4
    apps = sorted(p["application"] for p in m["plans"])
    assert apps == ["distribution", "procurement", "production", "replenishment"]


def test_workspace_is_deterministic_and_content_addressed():
    a = workspaces()
    b = workspaces()
    assert a.to_json() == b.to_json()
    assert a.workspace_id == b.workspace_id
    c = workspaces(created_at="2026-08-18T14:00:00Z")
    assert a.workspace_id != c.workspace_id


def test_workspace_is_immutable():
    ws = workspaces()
    with pytest.raises(FrozenInstanceError):
        ws.created_at = "mutated"


def test_default_launchers_compose_existing_contracts():
    args = ws_args()
    apps = {
        "replenishment": launch_replenishment_plan(
            OptimizedReplenishmentObservation(
                product_id="P", location_id="W", demands=(5.0,),
                evidence_ids=("e1",), provenance_ids=("p1",),
            ),
            command_id_prefix="cmd-1",
            **args,
        ),
        "procurement": launch_procurement_plan(
            OptimizedProcurementObservation(
                item_id="I", shortages=(5.0,),
                evidence_ids=("e1",), provenance_ids=("p1",),
            ),
            command_id_prefix="cmd-2",
            **args,
        ),
        "production": launch_production_plan(
            OptimizedProductionObservation(
                resource_id="R", requirements=(5.0,), capacity=10.0,
                evidence_ids=("e1",), provenance_ids=("p1",),
            ),
            command_id_prefix="cmd-3",
            **args,
        ),
        "distribution": launch_distribution_plan(
            OptimizedDistributionObservation(
                shipment_id="S", item_id="I", required_quantities=(5.0,),
                capacity=10.0, origin_location_id="A", destination_location_id="B",
                evidence_ids=("e1",), provenance_ids=("p1",),
            ),
            command_id_prefix="cmd-4",
            **args,
        ),
    }
    for app in ("replenishment", "procurement", "production", "distribution"):
        assert apps[app].application == app
        assert apps[app].period_count == 1


def test_workspace_plan_rejects_non_plan():
    with pytest.raises(WorkspaceError, match="unsupported plan artifact"):
        workspace_plan(object(), created_at="T")


def test_workspace_scenario_rejects_non_simulation():
    with pytest.raises(WorkspaceError, match="GovernedSimulationResult"):
        WorkspaceScenario(
            scenario_id="x", context_id="c", created_at="T", step_count=0,
            actionable_steps=0, no_action_steps=0, artifact=object(),
        )


def test_build_rejects_empty():
    with pytest.raises(WorkspaceError, match="at least one scenario or plan"):
        build_workspace_state(scenarios=(), plans=(), **{"created_at": "T", "view_actor_id": "a"})


def test_build_rejects_blank_created_at():
    with pytest.raises(WorkspaceError, match="created_at"):
        build_workspace_state(scenarios=(scenario(),), plans=(), **{"created_at": "", "view_actor_id": "a"})


def test_build_rejects_duplicate_scenario_id():
    a = scenario()
    b = scenario()
    with pytest.raises(WorkspaceError, match="scenario ids must be unique"):
        build_workspace_state(scenarios=(a, b), plans=(), **{"created_at": "T", "view_actor_id": "a"})


def test_build_rejects_non_scenario():
    with pytest.raises(WorkspaceError, match="every scenario"):
        build_workspace_state(scenarios=(object(),), plans=(), **{"created_at": "T", "view_actor_id": "a"})


def test_build_rejects_non_plan():
    with pytest.raises(WorkspaceError, match="every plan"):
        build_workspace_state(scenarios=(), plans=(object(),), **{"created_at": "T", "view_actor_id": "a"})
