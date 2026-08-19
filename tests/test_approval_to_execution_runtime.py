import pytest

from scm_ontology.approval_to_execution_runtime import (
    ApprovalToExecutionError,
    ApprovalToExecutionResult,
    approve_and_execute,
    build_approved_lifecycle,
)
from scm_ontology.command_lifecycle import (
    CommandState,
    start_command_lifecycle,
    transition_command,
)
from scm_ontology.decision_authorization import AuthorizedDecision
from scm_ontology.execution_command import build_execution_command
from scm_ontology.external_execution_adapter import (
    ExternalExecutionError,
    InMemoryExternalSystem,
    ReferenceExternalExecutionAdapter,
)
from scm_ontology.proposal_validation import ValidatedDecisionProposal
from scm_ontology.reasoning_output import ReasoningOutput


def command(proposal=None):
    output = ReasoningOutput(
        context_id="ctx-1",
        proposal=proposal or {"action": "replenish"},
        rationale="stock is below threshold",
        evidence_ids=("e1",),
        provenance_ids=("p1",),
        confidence=0.9,
    )
    decision = AuthorizedDecision(
        proposal=ValidatedDecisionProposal(output=output),
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-19T00:00:00Z",
    )
    return build_execution_command(
        decision, command_type="replenishment", command_id="cmd-1"
    )


def dry_run_lifecycle(command_id="cmd-1", recorded_at="2026-08-19T00:30:00Z", actor="planner-1"):
    lifecycle = build_approved_lifecycle(command_id, recorded_at=recorded_at, actor_id=actor)
    return transition_command(
        lifecycle,
        to_state=CommandState.DRY_RUN,
        occurred_at=recorded_at,
        actor_id=actor,
        reason="dry run",
    )


def test_approve_and_execute_reaches_executed_state():
    system = InMemoryExternalSystem()
    result = approve_and_execute(
        command(),
        adapter=ReferenceExternalExecutionAdapter(),
        executed_at="2026-08-19T01:00:00Z",
        actor_id="planner-1",
        lifecycle=dry_run_lifecycle(),
        external_system=system,
    )
    assert isinstance(result, ApprovalToExecutionResult)
    assert result.lifecycle.state == CommandState.EXECUTED
    assert result.verdict == "success"
    assert result.command_id == "cmd-1"
    assert system.write_count == 1
    # lifecycle transition history: proposed->authorized->approved->dry_run->executing->executed
    states = [t.to_state for t in result.lifecycle.transitions]
    assert states == [
        CommandState.AUTHORIZED,
        CommandState.APPROVED,
        CommandState.DRY_RUN,
        CommandState.EXECUTING,
        CommandState.EXECUTED,
    ]


def test_auto_builds_lifecycle_when_none_provided():
    result = approve_and_execute(
        command(),
        adapter=ReferenceExternalExecutionAdapter(),
        executed_at="2026-08-19T01:00:00Z",
        actor_id="planner-1",
    )
    assert result.lifecycle.state == CommandState.EXECUTED
    assert result.verdict == "success"


def test_fail_closed_when_lifecycle_not_at_dry_run():
    # Lifecycle at proposed — must not be executable.
    lifecycle = start_command_lifecycle("cmd-1")
    with pytest.raises(ApprovalToExecutionError):
        approve_and_execute(
            command(),
            adapter=ReferenceExternalExecutionAdapter(),
            executed_at="2026-08-19T01:00:00Z",
            actor_id="planner-1",
            lifecycle=lifecycle,
        )


def test_fail_closed_on_unsupported_command():
    from scm_ontology.decision_authorization import AuthorizedDecision

    output = ReasoningOutput(
        context_id="ctx-2",
        proposal={"action": "schedule"},
        rationale="x",
        evidence_ids=("e1",),
        provenance_ids=("p1",),
        confidence=0.5,
    )
    decision = AuthorizedDecision(
        proposal=ValidatedDecisionProposal(output=output),
        actor_id="planner-1",
        authority="manager",
        authorized_at="2026-08-19T00:00:00Z",
    )
    cmd = build_execution_command(decision, command_type="scheduling", command_id="cmd-9")
    with pytest.raises((ApprovalToExecutionError, ExternalExecutionError)):
        approve_and_execute(
            cmd,
            adapter=ReferenceExternalExecutionAdapter(),
            executed_at="2026-08-19T01:00:00Z",
            actor_id="planner-1",
        )


def test_fault_outcome_flow():
    result = approve_and_execute(
        command(proposal={"action": "replenish", "simulate_failure": True}),
        adapter=ReferenceExternalExecutionAdapter(),
        executed_at="2026-08-19T01:00:00Z",
        actor_id="planner-1",
    )
    assert result.lifecycle.state == CommandState.EXECUTED
    assert result.verdict == "failure"


def test_result_is_deterministic_and_immutable():
    a = approve_and_execute(
        command(),
        adapter=ReferenceExternalExecutionAdapter(),
        executed_at="2026-08-19T01:00:00Z",
        actor_id="planner-1",
    )
    b = approve_and_execute(
        command(),
        adapter=ReferenceExternalExecutionAdapter(),
        executed_at="2026-08-19T01:00:00Z",
        actor_id="planner-1",
    )
    assert a.to_json() == b.to_json()
    from dataclasses import FrozenInstanceError

    with pytest.raises(FrozenInstanceError):
        a.verdict = "failure"  # type: ignore[misc]


def test_missing_actor_fails_closed():
    with pytest.raises(ApprovalToExecutionError):
        approve_and_execute(
            command(),
            adapter=ReferenceExternalExecutionAdapter(),
            executed_at="2026-08-19T01:00:00Z",
            actor_id=" ",
        )
