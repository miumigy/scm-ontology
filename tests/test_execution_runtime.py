from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.decision_runtime import MockReasoningProvider
from scm_ontology.execution_command import ExecutionCommand
from scm_ontology.execution_runtime import (
    DryRunExecutionResult,
    DryRunPlan,
    ExecutionRuntimeError,
    InProcessDryRunAdapter,
    execute_dry_run,
    run_governed_loop_and_dry_run,
)
from scm_ontology.graph_reasoning_projection import GraphReasoningObservation


class StubAdapter:
    adapter_id = "stub-adapter"

    def dry_run(self, command):
        return {
            "execution_target": "erp",
            "action": command.decision.proposal.output.proposal["action"],
            "payload": {"proposal": command.decision.proposal.output.proposal},
            "detail": "stub plan",
        }


def observation():
    return GraphReasoningObservation(
        question_id="warehouse-stock",
        value={"warehouse": "WH-1", "stock": 5, "threshold": 10},
        evidence_ids=("e-stock-1",),
        provenance_ids=("p-erp-1",),
    )


def run_command():
    result = run_governed_loop_and_dry_run(
        context_id="ctx-r3",
        observations=(observation(),),
        provider=MockReasoningProvider(
            provider_id="mock",
            proposal={"action": "replenish", "quantity": 10},
            rationale="low stock",
            confidence=0.9,
        ),
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-17T21:00:00Z",
        command_type="replenishment",
        command_id="cmd-r3-1",
        dry_ran_at="2026-08-17T21:00:01Z",
    )
    return result.decision.execution_command


def test_execute_dry_run_returns_immutable_result():
    command = run_command()
    result = execute_dry_run(command, dry_ran_at="2026-08-17T21:00:01Z")
    assert isinstance(result, DryRunExecutionResult)
    assert result.command_id == "cmd-r3-1"
    assert result.context_id == "ctx-r3"
    assert result.status == "dry-run"
    assert result.plan.action == "replenish"
    assert result.plan.execution_target == "in-memory-dry-run"


def test_execute_dry_run_preserves_evidence_and_provenance():
    command = run_command()
    result = execute_dry_run(command, dry_ran_at="t")
    mapping = result.to_mapping()
    assert mapping["command"]["evidence_ids"] == ["e-stock-1"]
    assert mapping["command"]["provenance_ids"] == ["p-erp-1"]
    assert mapping["plan"]["payload"]["authority"] == "supply-chain-manager"


def test_execute_dry_run_is_deterministic():
    command = run_command()
    a = execute_dry_run(command, dry_ran_at="2026-08-17T21:00:01Z")
    b = execute_dry_run(command, dry_ran_at="2026-08-17T21:00:01Z")
    assert a.result_id == b.result_id
    assert a.to_json() == b.to_json()


def test_execute_dry_run_honors_custom_adapter():
    command = run_command()
    result = execute_dry_run(command, dry_ran_at="t", adapter=StubAdapter())
    assert result.plan.execution_target == "erp"
    assert result.plan.action == "replenish"
    assert result.plan.detail == "stub plan"


def test_execute_dry_run_rejects_non_command():
    with pytest.raises(ExecutionRuntimeError, match="must be an ExecutionCommand"):
        execute_dry_run(object(), dry_ran_at="t")


def test_execute_dry_run_rejects_blank_timestamp():
    command = run_command()
    with pytest.raises(ExecutionRuntimeError, match="dry_ran_at must be non-empty"):
        execute_dry_run(command, dry_ran_at="  ")


def test_execute_dry_run_rejects_invalid_adapter():
    command = run_command()
    with pytest.raises(ExecutionRuntimeError, match="adapter_id"):
        execute_dry_run(command, dry_ran_at="t", adapter=object())

    class NoDryRun:
        adapter_id = "x"

    with pytest.raises(ExecutionRuntimeError, match="callable dry_run"):
        execute_dry_run(command, dry_ran_at="t", adapter=NoDryRun())

    class NotADict:
        adapter_id = "x"

        def dry_run(self, command):
            return "not-a-plan"

    with pytest.raises(ExecutionRuntimeError, match="must return a mapping"):
        execute_dry_run(command, dry_ran_at="t", adapter=NotADict())


def test_execute_dry_run_wraps_adapter_failure():
    class Boom:
        adapter_id = "x"

        def dry_run(self, command):
            raise RuntimeError("adapter exploded")

    command = run_command()
    with pytest.raises(ExecutionRuntimeError, match="dry run failed: adapter exploded"):
        execute_dry_run(command, dry_ran_at="t", adapter=Boom())


def test_dry_run_plan_validates_target_action_payload():
    with pytest.raises(ExecutionRuntimeError, match="execution_target must be non-empty"):
        DryRunPlan(execution_target="", action="a", payload={})
    with pytest.raises(ExecutionRuntimeError, match="action must be non-empty"):
        DryRunPlan(execution_target="t", action="", payload={})


def test_full_governed_loop_and_dry_run_is_end_to_end():
    result = run_governed_loop_and_dry_run(
        context_id="ctx-r3-full",
        observations=(observation(),),
        provider=MockReasoningProvider(
            provider_id="mock",
            proposal={"action": "replenish", "quantity": 10},
            rationale="low stock",
        ),
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-17T21:00:00Z",
        command_type="replenishment",
        command_id="cmd-r3-full",
        dry_ran_at="2026-08-17T21:00:01Z",
    )
    assert result.context_id == "ctx-r3-full"
    assert result.dry_run.command_id == "cmd-r3-full"
    assert result.decision.execution_command.command_type == "replenishment"
    assert result.to_mapping()["dry_run"]["status"] == "dry-run"


def test_dry_run_result_artifacts_are_immutable():
    command = run_command()
    result = execute_dry_run(command, dry_ran_at="t")
    for obj in (result, result.plan):
        with pytest.raises(FrozenInstanceError):
            obj.status = "changed"


def test_dry_run_has_no_side_effects(tmp_path):
    sentinel = tmp_path / "side-effect"
    assert not sentinel.exists()
    command = run_command()
    execute_dry_run(command, dry_ran_at="t")
    assert not sentinel.exists()
    assert set(tmp_path.iterdir()) == set()
