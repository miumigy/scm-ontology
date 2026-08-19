import pytest

from scm_ontology.governed_simulation import SimulationApplication, SimulationStep
from scm_ontology.replenishment_application import ReplenishmentObservation
from scm_ontology.simulation_before_execution import (
    AgentSimulationEvaluation,
    SimulationBeforeExecutionError,
    evaluate_simulation_before_execution,
)


def _step(step_id="step-1", command_id="cmd-1"):
    return SimulationStep(
        step_id=step_id,
        application=SimulationApplication.REPLENISHMENT,
        observation=ReplenishmentObservation(
            product_id="p-1",
            location_id="loc-1",
            on_hand=5,
            reorder_point=10,
            reorder_quantity=20,
            evidence_ids=("e-inv",),
            provenance_ids=("p-inv",),
        ),
        command_id=command_id,
    )


def test_evaluation_runs_deterministic_simulation_before_execution():
    ev = evaluate_simulation_before_execution(
        context_id="ctx-1",
        steps=(_step(),),
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-19T01:00:00Z",
        dry_ran_at="2026-08-19T01:00:00Z",
    )
    assert isinstance(ev, AgentSimulationEvaluation)
    assert ev.feasible is True
    assert ev.simulation_result.simulation_run_id
    assert len(ev.simulation_result.steps) == 1
    assert "cmd-1" in ev.simulated_command_ids
    assert ev.evaluation_id


def test_evaluation_is_deterministic():
    kw = dict(
        context_id="ctx-1",
        steps=(_step(),),
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-19T01:00:00Z",
        dry_ran_at="2026-08-19T01:00:00Z",
    )
    a = evaluate_simulation_before_execution(**kw)
    b = evaluate_simulation_before_execution(**kw)
    assert a.to_json() == b.to_json()
    assert a.evaluation_id == b.evaluation_id


def test_infeasible_simulation_blocks_authorization_guidance():
    ev = evaluate_simulation_before_execution(
        context_id="ctx-1",
        steps=(_step(),),
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-19T01:00:00Z",
        dry_ran_at="2026-08-19T01:00:00Z",
        simulation_is_feasible=False,
    )
    assert ev.feasible is False
    assert "not feasible" in ev.rationale


def test_evaluation_fails_closed_on_blank_context():
    with pytest.raises(SimulationBeforeExecutionError):
        evaluate_simulation_before_execution(
            context_id=" ",
            steps=(_step(),),
            actor_id="planner-1",
            authority="supply-chain-manager",
            authorized_at="2026-08-19T01:00:00Z",
            dry_ran_at="2026-08-19T01:00:00Z",
        )


def test_evaluation_requires_at_least_one_step():
    with pytest.raises(SimulationBeforeExecutionError):
        evaluate_simulation_before_execution(
            context_id="ctx-1",
            steps=(),
            actor_id="planner-1",
            authority="supply-chain-manager",
            authorized_at="2026-08-19T01:00:00Z",
            dry_ran_at="2026-08-19T01:00:00Z",
        )
