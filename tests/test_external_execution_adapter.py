import pytest

from scm_ontology.decision_authorization import AuthorizedDecision
from scm_ontology.execution_command import build_execution_command
from scm_ontology.execution_outcome_contract import ExecutionOutcomeContract
from scm_ontology.external_execution_adapter import (
    ExternalExecutionError,
    InMemoryExternalSystem,
    ReferenceExternalExecutionAdapter,
    execute_externally,
    validate_external_adapter,
)
from scm_ontology.proposal_validation import ValidatedDecisionProposal
from scm_ontology.reasoning_output import ReasoningOutput


def command(proposal=None, command_type="replenishment", command_id="cmd-1"):
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
        decision, command_type=command_type, command_id=command_id
    )


def test_adapter_supports_reference_command_types():
    adapter = ReferenceExternalExecutionAdapter()
    assert adapter.supports("replenishment")
    assert adapter.supports("procurement")
    assert adapter.supports("production")
    assert adapter.supports("distribution")
    assert not adapter.supports("scheduling")
    validate_external_adapter(adapter)


def test_successful_execution_writes_to_external_system():
    system = InMemoryExternalSystem()
    adapter = ReferenceExternalExecutionAdapter()
    outcome = execute_externally(
        command(), adapter=adapter, executed_at="2026-08-19T01:00:00Z", external_system=system
    )
    assert isinstance(outcome, ExecutionOutcomeContract)
    assert outcome.verdict == "success"
    assert system.write_count == 1
    assert system.records[0].command_id == "cmd-1"
    assert system.records[0].status == "success"
    assert system.records[0].external_reference == "EXT-cmd-1-OK"


def test_failure_execution_is_controllable_via_proposal():
    system = InMemoryExternalSystem()
    adapter = ReferenceExternalExecutionAdapter()
    outcome = execute_externally(
        command(proposal={"action": "replenish", "simulate_failure": True}),
        adapter=adapter,
        executed_at="2026-08-19T01:00:00Z",
        external_system=system,
    )
    assert outcome.verdict == "failure"
    assert system.write_count == 1
    assert system.records[0].status == "failure"


def test_partial_execution_is_controllable_via_proposal():
    adapter = ReferenceExternalExecutionAdapter()
    outcome = execute_externally(
        command(proposal={"action": "replenish", "simulate_partial": True}),
        adapter=adapter,
        executed_at="2026-08-19T01:00:00Z",
    )
    assert outcome.verdict == "partial"
    assert len(outcome.elements) == 2


def test_execution_is_deterministic():
    a = execute_externally(
        command(), adapter=ReferenceExternalExecutionAdapter(), executed_at="2026-08-19T01:00:00Z"
    )
    b = execute_externally(
        command(), adapter=ReferenceExternalExecutionAdapter(), executed_at="2026-08-19T01:00:00Z"
    )
    assert a.to_json() == b.to_json()


def test_unsupported_command_type_fails_closed():
    adapter = ReferenceExternalExecutionAdapter()
    with pytest.raises(ExternalExecutionError):
        execute_externally(
            command(command_type="scheduling"),
            adapter=adapter,
            executed_at="2026-08-19T01:00:00Z",
        )


def test_invalid_adapter_fails_closed():
    class BadAdapter:
        pass

    with pytest.raises(ExternalExecutionError):
        execute_externally(command(), adapter=BadAdapter(), executed_at="2026-08-19T01:00:00Z")


def test_adapter_must_return_outcome_contract():
    class BadReturning:
        adapter_id = "bad"
        external_system = None

        def supports(self, command_type):
            return True

        def execute(self, command, *, executed_at, external_system=None):
            return {"nope": True}

    with pytest.raises(ExternalExecutionError):
        execute_externally(command(), adapter=BadReturning(), executed_at="2026-08-19T01:00:00Z")


def test_in_memory_external_system_isolated_between_instances():
    s1 = InMemoryExternalSystem()
    s2 = InMemoryExternalSystem()
    execute_externally(command(), adapter=ReferenceExternalExecutionAdapter(), executed_at="2026-08-19T01:00:00Z", external_system=s1)
    assert s1.write_count == 1
    assert s2.write_count == 0
