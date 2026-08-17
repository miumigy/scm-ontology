from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.production_application import (
    ProductionApplicationError,
    ProductionObservation,
    run_production_application,
)


def observation(required=80.0, capacity=100.0):
    return ProductionObservation(
        resource_id="LINE-1",
        required=required,
        capacity=capacity,
        unit="unit",
        evidence_ids=("e-capacity-1",),
        provenance_ids=("p-mes-1",),
    )


def run_args(**overrides):
    args = dict(
        context_id="ctx-r5-prod",
        actor_id="planner-1",
        authority="production-manager",
        authorized_at="2026-08-17T21:00:00Z",
        command_id="cmd-r5-prod",
        dry_ran_at="2026-08-17T21:00:01Z",
    )
    args.update(overrides)
    return args


def test_feasible_requirement_schedules_production():
    decision = run_production_application(observation(required=80.0, capacity=100.0), **run_args())
    assert decision.is_schedule is True
    assert decision.resource_id == "LINE-1"
    assert decision.quantity == 80.0
    governed = decision.governed
    assert governed is not None
    command = governed.decision.execution_command
    assert command.context_id == "ctx-r5-prod"
    assert command.command_type == "production-order"
    assert command.command_id == "cmd-r5-prod"
    assert governed.dry_run.plan.action == "schedule"


def test_schedule_preserves_evidence_and_provenance():
    decision = run_production_application(observation(required=80.0, capacity=100.0), **run_args())
    command_mapping = decision.governed.decision.execution_command.to_mapping()
    assert command_mapping["evidence_ids"] == ["e-capacity-1"]
    assert command_mapping["provenance_ids"] == ["p-mes-1"]


def test_infeasible_requirement_escalates_without_command():
    decision = run_production_application(observation(required=120.0, capacity=100.0), **run_args())
    assert decision.action == "escalate"
    assert decision.is_schedule is False
    assert decision.quantity == 0.0
    assert decision.governed is None


def test_exact_capacity_is_feasible():
    decision = run_production_application(observation(required=100.0, capacity=100.0), **run_args())
    assert decision.is_schedule is True
    assert decision.governed is not None


def test_application_is_deterministic():
    a = run_production_application(observation(required=80.0, capacity=100.0), **run_args())
    b = run_production_application(observation(required=80.0, capacity=100.0), **run_args())
    assert a.to_mapping()["governed"]["dry_run"]["result_id"] == b.to_mapping()["governed"]["dry_run"]["result_id"]


def test_application_validates_inputs():
    with pytest.raises(ProductionApplicationError, match="resource_id"):
        ProductionObservation(resource_id="", required=1.0, capacity=2.0)
    with pytest.raises(ProductionApplicationError, match="required"):
        ProductionObservation(resource_id="R", required=-1.0, capacity=2.0)
    with pytest.raises(ProductionApplicationError, match="context_id"):
        run_production_application(observation(), **run_args(context_id=""))
    with pytest.raises(ProductionApplicationError, match="ProductionObservation"):
        run_production_application(object(), **run_args())


def test_observation_projection_is_deterministic():
    obs = observation(required=80.0, capacity=100.0)
    projected = obs.to_observation("ctx-x")
    assert projected.question_id == "capacity-requirement"
    assert projected.value["required"] == 80.0
    assert projected.value["capacity"] == 100.0
    assert projected.evidence_ids == ("e-capacity-1",)


def test_decision_is_immutable():
    decision = run_production_application(observation(required=80.0, capacity=100.0), **run_args())
    with pytest.raises(FrozenInstanceError):
        decision.action = "halt"
