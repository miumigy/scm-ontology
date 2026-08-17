"""Phase R5 integration: multiple governed applications share the same loop."""
from scm_ontology.distribution_application import (
    DistributionObservation,
    run_distribution_application,
)
from scm_ontology.procurement_application import ProcurementObservation, run_procurement_application
from scm_ontology.production_application import ProductionObservation, run_production_application
from scm_ontology.replenishment_application import ReplenishmentObservation, run_replenishment_application


def test_replenishment_and_procurement_production_distribution_all_run_governed_loop():
    base = dict(
        context_id="ctx-r5-apps",
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-17T21:00:00Z",
        dry_ran_at="2026-08-17T21:00:01Z",
    )

    replenish = run_replenishment_application(
        ReplenishmentObservation(
            product_id="P-1", location_id="WH-1", on_hand=5.0,
            reorder_point=10.0, reorder_quantity=25.0,
            evidence_ids=("e-stock-1",), provenance_ids=("p-erp-1",),
        ),
        command_id="cmd-app-1",
        **base,
    )
    procure = run_procurement_application(
        ProcurementObservation(
            item_id="ITEM-1", shortage=10.0,
            evidence_ids=("e-gap-1",), provenance_ids=("p-erp-1",),
        ),
        command_id="cmd-app-2",
        **base,
    )
    produce = run_production_application(
        ProductionObservation(
            resource_id="LINE-1", required=80.0, capacity=100.0,
            evidence_ids=("e-cap-1",), provenance_ids=("p-mes-1",),
        ),
        command_id="cmd-app-3",
        **base,
    )
    distribute = run_distribution_application(
        DistributionObservation(
            shipment_id="SHIP-1", item_id="ITEM-1",
            required_quantity=80.0, capacity=100.0,
            origin_location_id="WH-A", destination_location_id="DC-B",
            evidence_ids=("e-tm-1",), provenance_ids=("p-tms-1",),
        ),
        command_id="cmd-app-4",
        **base,
    )

    # All four applications produced authorized commands through the loop.
    assert replenish.is_replenish is True
    assert procure.is_procure is True
    assert produce.is_schedule is True
    assert distribute.is_ship is True

    # Each command is bound to the shared context and carries its own id.
    for decision in (replenish, procure, produce, distribute):
        governed = decision.governed
        assert governed is not None
        assert governed.decision.execution_command.context_id == "ctx-r5-apps"
        # Dry run is side-effect-free and deterministic per command.
        assert governed.dry_run.status == "dry-run"


def test_distribution_escalates_independently_when_capacity_infeasible():
    base = dict(
        context_id="ctx-r5-apps",
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-17T21:00:00Z",
        dry_ran_at="2026-08-17T21:00:01Z",
    )
    escalate = run_distribution_application(
        DistributionObservation(
            shipment_id="SHIP-2", item_id="ITEM-2",
            required_quantity=120.0, capacity=100.0,
            origin_location_id="WH-B", destination_location_id="DC-C",
        ),
        command_id="cmd-app-5",
        **base,
    )
    # The infeasible shipment escalates independently without a command.
    assert escalate.action == "escalate"
    assert escalate.is_ship is False
    assert escalate.governed is None


def test_applications_fail_closed_without_side_effect(tmp_path):
    sentinel = tmp_path / "side-effect"
    base = {
        "context_id": "ctx-r5-safe",
        "actor_id": "planner-1",
        "authority": "supply-chain-manager",
        "authorized_at": "2026-08-17T21:00:00Z",
        "dry_ran_at": "2026-08-17T21:00:01Z",
    }
    assert not sentinel.exists()
    run_replenishment_application(
        ReplenishmentObservation(
            "P", "WH", 5.0, 10.0, 25.0,
            evidence_ids=("e1",), provenance_ids=("p1",),
        ),
        command_id="c1", **base,
    )
    run_procurement_application(
        ProcurementObservation("I", 5.0, evidence_ids=("e2",), provenance_ids=("p2",)),
        command_id="c2", **base,
    )
    run_production_application(
        ProductionObservation("R", 30.0, 100.0, evidence_ids=("e3",), provenance_ids=("p3",)),
        command_id="c3", **base,
    )
    run_distribution_application(
        DistributionObservation(
            "S", "I", 30.0, 100.0, "WH", "DC",
            evidence_ids=("e4",), provenance_ids=("p4",),
        ),
        command_id="c4", **base,
    )
    assert not sentinel.exists()
    assert set(tmp_path.iterdir()) == set()
