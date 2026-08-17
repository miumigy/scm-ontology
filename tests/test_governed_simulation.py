from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.governed_simulation import (
    GovernedSimulationError,
    GovernedSimulationResult,
    SimulationApplication,
    SimulationStep,
    run_governed_simulation,
)
from scm_ontology.replenishment_application import ReplenishmentObservation
from scm_ontology.procurement_application import ProcurementObservation
from scm_ontology.production_application import ProductionObservation
from scm_ontology.distribution_application import DistributionObservation


def run_args(**overrides):
    args = dict(
        context_id="ctx-r5-sim",
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-17T21:00:00Z",
        dry_ran_at="2026-08-17T21:00:01Z",
    )
    args.update(overrides)
    return args


def steps():
    return (
        SimulationStep(
            step_id="s1",
            application=SimulationApplication.REPLENISHMENT,
            observation=ReplenishmentObservation(
                product_id="P-1", location_id="WH-1", on_hand=5.0,
                reorder_point=10.0, reorder_quantity=25.0,
                evidence_ids=("e-stock-1",), provenance_ids=("p-erp-1",),
            ),
            command_id="cmd-1",
        ),
        SimulationStep(
            step_id="s2",
            application=SimulationApplication.PRODUCTION,
            observation=ProductionObservation(
                resource_id="LINE-1", required=80.0, capacity=100.0,
                evidence_ids=("e-cap-1",), provenance_ids=("p-mes-1",),
            ),
            command_id="cmd-2",
        ),
        SimulationStep(
            step_id="s3",
            application=SimulationApplication.DISTRIBUTION,
            observation=DistributionObservation(
                shipment_id="SHIP-1", item_id="P-1",
                required_quantity=80.0, capacity=100.0,
                origin_location_id="WH-1", destination_location_id="DC-1",
                evidence_ids=("e-tm-1",), provenance_ids=("p-tms-1",),
            ),
            command_id="cmd-3",
        ),
    )


def test_multi_step_simulation_runs_all_governed_loops():
    result = run_governed_simulation(steps(), **run_args())
    assert isinstance(result, GovernedSimulationResult)
    assert result.to_mapping()["contract_version"] == "S363.1"
    assert len(result.steps) == 3
    actions = [step.action for step in result.steps]
    assert actions == ["replenish", "schedule", "ship"]
    # Each governed decision carries a dry-run result.
    for step in result.steps:
        governed = step.decision.governed
        assert governed is not None
        assert governed.decision.execution_command.context_id == "ctx-r5-sim"
        assert governed.dry_run.status == "dry-run"


def test_all_four_applications_are_supported():
    four = (
        SimulationStep(
            step_id="p1",
            application=SimulationApplication.PROCUREMENT,
            observation=ProcurementObservation(
                item_id="ITEM-1", shortage=10.0,
                evidence_ids=("e-gap-1",), provenance_ids=("p-erp-1",),
            ),
            command_id="cmd-p",
        ),
    ) + steps()
    result = run_governed_simulation(four, **run_args())
    assert len(result.steps) == 4
    assert result.steps[0].application == "procurement"
    assert result.steps[0].action == "procure"


def test_no_action_step_records_no_command():
    no_action_steps = (
        SimulationStep(
            step_id="s1",
            application=SimulationApplication.REPLENISHMENT,
            observation=ReplenishmentObservation(
                product_id="P-2", location_id="WH-2", on_hand=20.0,
                reorder_point=10.0, reorder_quantity=25.0,
                evidence_ids=("e1",), provenance_ids=("p1",),
            ),
            command_id="cmd-1",
        ),
    )
    result = run_governed_simulation(no_action_steps, **run_args())
    assert result.steps[0].action == "no_replenishment"
    assert result.steps[0].decision.governed is None
    assert result.steps[0].decision.is_replenish is False


def test_escalate_step_records_no_command():
    escalate_steps = (
        SimulationStep(
            step_id="s1",
            application=SimulationApplication.DISTRIBUTION,
            observation=DistributionObservation(
                shipment_id="SHIP-9", item_id="I",
                required_quantity=120.0, capacity=100.0,
                origin_location_id="WH", destination_location_id="DC",
                evidence_ids=("e1",), provenance_ids=("p1",),
            ),
            command_id="cmd-1",
        ),
    )
    result = run_governed_simulation(escalate_steps, **run_args())
    assert result.steps[0].action == "escalate"
    assert result.steps[0].decision.governed is None


def test_simulation_is_deterministic():
    a = run_governed_simulation(steps(), **run_args())
    b = run_governed_simulation(steps(), **run_args())
    assert a.simulation_run_id == b.simulation_run_id
    assert a.to_json() == b.to_json()


def test_simulation_preserves_evidence_and_provenance_per_step():
    result = run_governed_simulation(steps(), **run_args())
    first = result.steps[0].decision
    mapping = first.governed.decision.execution_command.to_mapping()
    assert mapping["evidence_ids"] == ["e-stock-1"]
    assert mapping["provenance_ids"] == ["p-erp-1"]


def test_simulation_rejects_empty_steps():
    with pytest.raises(GovernedSimulationError, match="steps must not be empty"):
        run_governed_simulation((), **run_args())


def test_simulation_rejects_duplicate_step_ids():
    dup = (steps()[0], steps()[0])
    with pytest.raises(GovernedSimulationError, match="unique"):
        run_governed_simulation(dup, **run_args())


def test_simulation_rejects_invalid_application():
    with pytest.raises(GovernedSimulationError, match="application"):
        SimulationStep(step_id="s1", application="bogus", observation=None, command_id="c1")


def test_simulation_rejects_invalid_observation():
    with pytest.raises(Exception):
        run_governed_simulation(
            (
                SimulationStep(
                    step_id="s1",
                    application=SimulationApplication.REPLENISHMENT,
                    observation=object(),
                    command_id="c1",
                ),
            ),
            **run_args(),
        )


def test_simulation_rejects_blank_context():
    with pytest.raises(GovernedSimulationError, match="context_id"):
        run_governed_simulation(steps(), **run_args(context_id=""))


def test_simulation_rejects_blank_actor_or_authority():
    with pytest.raises(GovernedSimulationError, match="actor_id"):
        run_governed_simulation(steps(), **run_args(actor_id=""))
    with pytest.raises(GovernedSimulationError, match="authority"):
        run_governed_simulation(steps(), **run_args(authority=""))


def test_simulation_result_is_immutable():
    result = run_governed_simulation(steps(), **run_args())
    with pytest.raises(FrozenInstanceError):
        result.context_id = "mutated"


def test_simulation_fails_closed_without_side_effect(tmp_path):
    sentinel = tmp_path / "side-effect"
    assert not sentinel.exists()
    run_governed_simulation(steps(), **run_args())
    assert not sentinel.exists()
    assert set(tmp_path.iterdir()) == set()
