from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.optimized_app_planning import (
    OptimizedAppPlanningError,
    OptimizedDistributionObservation,
    OptimizedProcurementObservation,
    OptimizedProductionObservation,
    run_optimized_distribution_planning,
    run_optimized_procurement_planning,
    run_optimized_production_planning,
)


def run_args(**overrides):
    args = dict(
        context_id="ctx-s365",
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-17T21:00:00Z",
        command_id_prefix="cmd-s365",
        dry_ran_at="2026-08-17T21:00:01Z",
    )
    args.update(overrides)
    return args


# ---------------------------------------------------------------------------
# Procurement (S360)
# ---------------------------------------------------------------------------
def test_optimized_procurement_procures_shortages_and_skips_zero():
    result = run_optimized_procurement_planning(
        OptimizedProcurementObservation(
            item_id="ITEM-1",
            shortages=(0.0, 50.0, 120.0, 0.0),
            evidence_ids=("e1",), provenance_ids=("p1",),
        ),
        **run_args(),
    )
    assert result.to_mapping()["contract_version"] == "S365.1"
    assert result.plan.plan_type == "procurement_plan"
    actions = [p.decision.action for p in result.periods]
    assert actions == ["no_procurement", "procure", "procure", "no_procurement"]
    assert result.periods[1].decision.governed is not None
    assert result.periods[0].decision.governed is None


def test_optimized_procurement_is_deterministic_and_json_safe():
    a = run_optimized_procurement_planning(
        OptimizedProcurementObservation(
            item_id="ITEM-1", shortages=(10.0, 20.0),
            evidence_ids=("e1",), provenance_ids=("p1",),
        ),
        **run_args(),
    )
    b = run_optimized_procurement_planning(
        OptimizedProcurementObservation(
            item_id="ITEM-1", shortages=(10.0, 20.0),
            evidence_ids=("e1",), provenance_ids=("p1",),
        ),
        **run_args(),
    )
    assert a.to_json() == b.to_json()
    assert '"period_index":0' in a.to_json()


# ---------------------------------------------------------------------------
# Production (S361)
# ---------------------------------------------------------------------------
def test_optimized_production_schedules_within_capacity_and_escalates_over():
    result = run_optimized_production_planning(
        OptimizedProductionObservation(
            resource_id="LINE-1",
            requirements=(80.0, 120.0, 50.0),
            capacity=100.0,
            evidence_ids=("e2",), provenance_ids=("p2",),
        ),
        **run_args(),
    )
    assert result.plan.plan_type == "production_plan"
    actions = [p.decision.action for p in result.periods]
    assert actions == ["schedule", "escalate", "schedule"]
    assert result.periods[0].decision.governed is not None
    assert result.periods[1].decision.governed is None  # over-capacity escalates
    assert result.periods[0].quantity == 80.0
    assert result.periods[1].quantity == 120.0


# ---------------------------------------------------------------------------
# Distribution (S362)
# ---------------------------------------------------------------------------
def test_optimized_distribution_ships_within_capacity_and_escalates_over():
    result = run_optimized_distribution_planning(
        OptimizedDistributionObservation(
            shipment_id="SHIP-1",
            item_id="ITEM-1",
            required_quantities=(80.0, 120.0, 50.0),
            capacity=100.0,
            origin_location_id="WH",
            destination_location_id="DC",
            evidence_ids=("e3",), provenance_ids=("p3",),
        ),
        **run_args(),
    )
    assert result.plan.plan_type == "distribution_plan"
    actions = [p.decision.action for p in result.periods]
    assert actions == ["ship", "escalate", "ship"]
    assert result.periods[0].decision.governed is not None
    assert result.periods[1].decision.governed is None
    assert result.periods[0].quantity == 80.0


# ---------------------------------------------------------------------------
# Shared behavior
# ---------------------------------------------------------------------------
def test_plans_carry_objectives_constraints_and_provenance():
    result = run_optimized_procurement_planning(
        OptimizedProcurementObservation(
            item_id="I", shortages=(5.0,),
            evidence_ids=("e-1",), provenance_ids=("p-1",),
        ),
        **run_args(),
    )
    assert "objective:match-shortage" in result.plan.objective_refs
    assert "constraint:no-excess-purchase" in result.plan.constraint_refs
    assert result.plan.provenance_refs == ("p-1",)
    assert result.plan.status.value == "proposed"


def test_evidence_and_provenance_preserved_through_governed_loop():
    result = run_optimized_procurement_planning(
        OptimizedProcurementObservation(
            item_id="ITEM-1", shortages=(10.0,),
            evidence_ids=("e-ev",), provenance_ids=("p-pr",),
        ),
        **run_args(),
    )
    procuring = next(p for p in result.periods if p.decision.action == "procure")
    mapping = procuring.decision.governed.decision.execution_command.to_mapping()
    assert mapping["evidence_ids"] == ["e-ev"]
    assert mapping["provenance_ids"] == ["p-pr"]


def test_validation_rejects_invalid_inputs():
    with pytest.raises(OptimizedAppPlanningError, match="item_id"):
        OptimizedProcurementObservation(item_id="", shortages=(1.0,))
    with pytest.raises(OptimizedAppPlanningError, match="non-empty tuple"):
        OptimizedProcurementObservation(item_id="I", shortages=())
    with pytest.raises(OptimizedAppPlanningError, match="non-negative"):
        OptimizedProcurementObservation(item_id="I", shortages=(-1.0,))
    with pytest.raises(OptimizedAppPlanningError, match="origin and destination"):
        OptimizedDistributionObservation(
            shipment_id="S", item_id="I", required_quantities=(1.0,),
            capacity=2.0, origin_location_id="A", destination_location_id="A",
        )
    with pytest.raises(OptimizedAppPlanningError, match="context_id"):
        run_optimized_procurement_planning(
            OptimizedProcurementObservation(item_id="I", shortages=(1.0,)),
            **run_args(context_id=""),
        )
    with pytest.raises(OptimizedAppPlanningError, match="OptimizedProcurementObservation"):
        run_optimized_procurement_planning(object(), **run_args())


def test_results_are_immutable():
    result = run_optimized_procurement_planning(
        OptimizedProcurementObservation(
            item_id="I", shortages=(5.0,),
            evidence_ids=("e-1",), provenance_ids=("p-1",),
        ),
        **run_args(),
    )
    with pytest.raises(FrozenInstanceError):
        result.plan = None


def test_fails_closed_without_side_effect(tmp_path):
    sentinel = tmp_path / "side-effect"
    assert not sentinel.exists()
    run_optimized_procurement_planning(
        OptimizedProcurementObservation(
            item_id="I", shortages=(5.0,),
            evidence_ids=("e1",), provenance_ids=("p1",),
        ),
        **run_args(),
    )
    run_optimized_production_planning(
        OptimizedProductionObservation(
            resource_id="R", requirements=(5.0,), capacity=10.0,
            evidence_ids=("e2",), provenance_ids=("p2",),
        ),
        **run_args(),
    )
    run_optimized_distribution_planning(
        OptimizedDistributionObservation(
            shipment_id="S", item_id="I", required_quantities=(5.0,), capacity=10.0,
            origin_location_id="WH", destination_location_id="DC",
            evidence_ids=("e3",), provenance_ids=("p3",),
        ),
        **run_args(),
    )
    assert not sentinel.exists()
    assert set(tmp_path.iterdir()) == set()
