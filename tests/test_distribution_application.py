from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.distribution_application import (
    DistributionApplicationError,
    DistributionObservation,
    run_distribution_application,
)


def observation(required=80.0, capacity=100.0):
    return DistributionObservation(
        shipment_id="SHIP-1",
        item_id="MAT-001",
        required_quantity=required,
        capacity=capacity,
        origin_location_id="WH-A",
        destination_location_id="DC-B",
        unit="unit",
        evidence_ids=("e-capacity-1",),
        provenance_ids=("p-tms-1",),
    )


def run_args(**overrides):
    args = dict(
        context_id="ctx-r5-dist",
        actor_id="planner-1",
        authority="distribution-manager",
        authorized_at="2026-08-17T21:00:00Z",
        command_id="cmd-r5-dist",
        dry_ran_at="2026-08-17T21:00:01Z",
    )
    args.update(overrides)
    return args


def test_feasible_requirement_ships():
    decision = run_distribution_application(observation(required=80.0, capacity=100.0), **run_args())
    assert decision.is_ship is True
    assert decision.shipment_id == "SHIP-1"
    assert decision.quantity == 80.0
    governed = decision.governed
    assert governed is not None
    command = governed.decision.execution_command
    assert command.context_id == "ctx-r5-dist"
    assert command.command_type == "shipment"
    assert command.command_id == "cmd-r5-dist"
    assert governed.dry_run.plan.action == "ship"


def test_ship_preserves_evidence_and_provenance():
    decision = run_distribution_application(observation(required=80.0, capacity=100.0), **run_args())
    command_mapping = decision.governed.decision.execution_command.to_mapping()
    assert command_mapping["evidence_ids"] == ["e-capacity-1"]
    assert command_mapping["provenance_ids"] == ["p-tms-1"]


def test_infeasible_requirement_escalates_without_command():
    decision = run_distribution_application(observation(required=120.0, capacity=100.0), **run_args())
    assert decision.action == "escalate"
    assert decision.is_ship is False
    assert decision.quantity == 0.0
    assert decision.governed is None


def test_exact_capacity_is_feasible():
    decision = run_distribution_application(observation(required=100.0, capacity=100.0), **run_args())
    assert decision.is_ship is True
    assert decision.governed is not None


def test_application_is_deterministic():
    a = run_distribution_application(observation(required=80.0, capacity=100.0), **run_args())
    b = run_distribution_application(observation(required=80.0, capacity=100.0), **run_args())
    assert a.to_mapping()["governed"]["dry_run"]["result_id"] == b.to_mapping()["governed"]["dry_run"]["result_id"]


def test_application_validates_inputs():
    with pytest.raises(DistributionApplicationError, match="shipment_id"):
        DistributionObservation(
            shipment_id="", item_id="M", required_quantity=1.0, capacity=2.0,
            origin_location_id="A", destination_location_id="B",
        )
    with pytest.raises(DistributionApplicationError, match="required_quantity"):
        DistributionObservation(
            shipment_id="S", item_id="M", required_quantity=-1.0, capacity=2.0,
            origin_location_id="A", destination_location_id="B",
        )
    with pytest.raises(DistributionApplicationError, match="origin and destination"):
        DistributionObservation(
            shipment_id="S", item_id="M", required_quantity=1.0, capacity=2.0,
            origin_location_id="A", destination_location_id="A",
        )
    with pytest.raises(DistributionApplicationError, match="context_id"):
        run_distribution_application(observation(), **run_args(context_id=""))
    with pytest.raises(DistributionApplicationError, match="DistributionObservation"):
        run_distribution_application(object(), **run_args())


def test_observation_projection_is_deterministic():
    obs = observation(required=80.0, capacity=100.0)
    projected = obs.to_observation("ctx-x")
    assert projected.question_id == "distribution-capacity"
    assert projected.value["required_quantity"] == 80.0
    assert projected.value["capacity"] == 100.0
    assert projected.value["origin_location_id"] == "WH-A"
    assert projected.value["destination_location_id"] == "DC-B"
    assert projected.evidence_ids == ("e-capacity-1",)


def test_decision_is_immutable():
    decision = run_distribution_application(observation(required=80.0, capacity=100.0), **run_args())
    with pytest.raises(FrozenInstanceError):
        decision.action = "halt"
