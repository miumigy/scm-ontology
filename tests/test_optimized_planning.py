from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.optimized_planning import (
    OptimizedPlanningError,
    OptimizedReplenishmentObservation,
    optimize_replenishment_quantities,
    run_optimized_planning,
)


def observation(**overrides):
    args = dict(
        product_id="P-1",
        location_id="WH-1",
        demands=(100.0, 0.0, 50.0, 120.0),
        initial_on_hand=0.0,
        reorder_point=0.0,
        unit="unit",
        evidence_ids=("e-demand-1",),
        provenance_ids=("p-erp-1",),
    )
    args.update(overrides)
    return OptimizedReplenishmentObservation(**args)


def run_args(**overrides):
    args = dict(
        context_id="ctx-s364",
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-17T21:00:00Z",
        command_id_prefix="cmd-s364",
        dry_ran_at="2026-08-17T21:00:01Z",
    )
    args.update(overrides)
    return args


def test_optimized_planning_runs_each_period_through_governed_loop():
    result = run_optimized_planning(observation(), **run_args())
    assert result.to_mapping()["contract_version"] == "S364.1"
    # demands (100, 0, 50, 120) with no initial on-hand -> replenish 100, 0, 50, 120
    actions = [p.decision.action for p in result.periods]
    assert actions == ["replenish", "no_replenishment", "replenish", "replenish"]
    # Replenishing periods carry a governed command; no-action does not.
    assert result.periods[0].decision.governed is not None
    assert result.periods[1].decision.governed is None
    assert result.periods[2].decision.governed is not None
    assert result.periods[3].decision.governed is not None
    assert result.total_replenishment == 270.0


def test_optimizer_uses_initial_on_hand():
    obs = observation(initial_on_hand=60.0)
    quantities = optimize_replenishment_quantities(obs)
    assert quantities == (40.0, 0.0, 50.0, 120.0)
    result = run_optimized_planning(obs, **run_args())
    assert result.total_replenishment == 210.0


def test_reorder_point_adds_safety_stock():
    obs = observation(demands=(100.0,), reorder_point=20.0)
    quantities = optimize_replenishment_quantities(obs)
    assert quantities == (120.0,)


def test_plan_carries_objective_constraint_and_provenance():
    result = run_optimized_planning(observation(), **run_args())
    assert result.plan.plan_type == "replenishment_plan"
    assert result.plan.status.value == "proposed"
    assert "objective:minimize-holding-cost" in result.plan.objective_refs
    assert "constraint:no-stockout" in result.plan.constraint_refs
    assert result.plan.provenance_refs == ("p-erp-1",)


def test_application_is_deterministic():
    a = run_optimized_planning(observation(), **run_args())
    b = run_optimized_planning(observation(), **run_args())
    assert a.to_json() == b.to_json()


def test_evidence_and_provenance_preserved():
    result = run_optimized_planning(observation(), **run_args())
    replenishing = next(p for p in result.periods if p.decision.action == "replenish")
    mapping = replenishing.decision.governed.decision.execution_command.to_mapping()
    assert mapping["evidence_ids"] == ["e-demand-1"]
    assert mapping["provenance_ids"] == ["p-erp-1"]


def test_application_validates_inputs():
    with pytest.raises(OptimizedPlanningError, match="product_id"):
        OptimizedReplenishmentObservation(product_id="", location_id="L", demands=(1.0,))
    with pytest.raises(OptimizedPlanningError, match="demands must be a non-empty"):
        OptimizedReplenishmentObservation(product_id="P", location_id="L", demands=())
    with pytest.raises(OptimizedPlanningError, match="non-negative"):
        OptimizedReplenishmentObservation(product_id="P", location_id="L", demands=(-1.0,))
    with pytest.raises(OptimizedPlanningError, match="context_id"):
        run_optimized_planning(observation(), **run_args(context_id=""))
    with pytest.raises(OptimizedPlanningError, match="OptimizedReplenishmentObservation"):
        run_optimized_planning(object(), **run_args())


def test_result_is_immutable():
    result = run_optimized_planning(observation(), **run_args())
    with pytest.raises(FrozenInstanceError):
        result.plan_ref = "mutated"


def test_fails_closed_without_side_effect(tmp_path):
    sentinel = tmp_path / "side-effect"
    assert not sentinel.exists()
    run_optimized_planning(observation(), **run_args())
    assert not sentinel.exists()
    assert set(tmp_path.iterdir()) == set()
