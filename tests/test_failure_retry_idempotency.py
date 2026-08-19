import pytest

from scm_ontology.decision_authorization import AuthorizedDecision
from scm_ontology.execution_command import build_execution_command
from scm_ontology.external_execution_adapter import ReferenceExternalExecutionAdapter
from scm_ontology.failure_retry_idempotency import (
    ExecutionAttempt,
    ExecutionRunRecord,
    ExecutionRunRegistry,
    FailureRetryError,
    RecoverySignal,
    RetryableAdapter,
    RunPolicy,
    run_with_failure_policy,
)
from scm_ontology.proposal_validation import ValidatedDecisionProposal
from scm_ontology.reasoning_output import ReasoningOutput


def command(command_id="cmd-1"):
    output = ReasoningOutput(
        context_id="ctx-1",
        proposal={"action": "replenish", "quantity": 20},
        rationale="stock low",
        evidence_ids=("e1",),
        provenance_ids=("p1",),
        confidence=0.9,
    )
    decision = AuthorizedDecision(
        proposal=ValidatedDecisionProposal(output=output),
        actor_id="planner-1",
        authority="manager",
        authorized_at="2026-08-19T00:00:00Z",
    )
    return build_execution_command(
        decision, command_type="replenishment", command_id=command_id
    )


def test_success_requires_single_attempt():
    registry = ExecutionRunRegistry()
    record = run_with_failure_policy(
        command(),
        adapter=ReferenceExternalExecutionAdapter(),
        policy=RunPolicy(max_attempts=3),
        registry=registry,
        actor_id="planner-1",
        executed_at="2026-08-19T01:00:00Z",
    )
    assert record.status == "executed"
    assert record.attempt_count == 1


def test_bounded_retry_recovers_after_transient_failure():
    registry = ExecutionRunRegistry()
    flaky = RetryableAdapter(ReferenceExternalExecutionAdapter(), failures_before_success=2)
    record = run_with_failure_policy(
        command(),
        adapter=flaky,
        policy=RunPolicy(max_attempts=4),
        registry=registry,
        actor_id="planner-1",
        executed_at="2026-08-19T01:00:00Z",
    )
    assert record.status == "executed"
    assert record.attempt_count == 3  # 2 failures + 1 success


def test_duplicate_command_is_not_re_executed():
    registry = ExecutionRunRegistry()
    adapter = ReferenceExternalExecutionAdapter()
    first = run_with_failure_policy(
        command(),
        adapter=adapter,
        policy=RunPolicy(max_attempts=3),
        registry=registry,
        actor_id="planner-1",
        executed_at="2026-08-19T01:00:00Z",
    )
    second = run_with_failure_policy(
        command(),
        adapter=adapter,
        policy=RunPolicy(max_attempts=3),
        registry=registry,
        actor_id="planner-1",
        executed_at="2026-08-19T02:00:00Z",
    )
    assert second is first
    assert first.attempt_count == 1


def test_retries_exhausted_records_failed_permanently_with_recovery():
    registry = ExecutionRunRegistry()
    always_fail = RetryableAdapter(
        ReferenceExternalExecutionAdapter(), failures_before_success=99
    )
    record = run_with_failure_policy(
        command(),
        adapter=always_fail,
        policy=RunPolicy(max_attempts=3),
        registry=registry,
        actor_id="planner-1",
        executed_at="2026-08-19T01:00:00Z",
    )
    assert record.status == "failed_permanently"
    assert record.attempt_count == 3
    assert record.recovery is not None
    assert record.recovery.command_id == "cmd-1"
    assert "manual intervention" in record.recovery.required_action


def test_partial_outcome_is_not_retried():
    registry = ExecutionRunRegistry()
    partial = RetryableAdapter(
        ReferenceExternalExecutionAdapter(),
        fail_partial_after=1,
    )
    record = run_with_failure_policy(
        command(),
        adapter=partial,
        policy=RunPolicy(max_attempts=5),
        registry=registry,
        actor_id="planner-1",
        executed_at="2026-08-19T01:00:00Z",
    )
    assert record.status == "partial"
    assert record.attempt_count == 1


def test_registry_prevents_overwrite():
    registry = ExecutionRunRegistry()
    first = run_with_failure_policy(
        command(),
        adapter=ReferenceExternalExecutionAdapter(),
        policy=RunPolicy(max_attempts=3),
        registry=registry,
        actor_id="planner-1",
        executed_at="2026-08-19T01:00:00Z",
    )
    with pytest.raises(FailureRetryError):
        registry.record(first)


def test_policy_requires_positive_max_attempts():
    with pytest.raises(FailureRetryError):
        RunPolicy(max_attempts=0)
