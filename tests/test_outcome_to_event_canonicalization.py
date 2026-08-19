import pytest

from scm_ontology.approval_to_execution_runtime import (
    approve_and_execute,
)
from scm_ontology.canonical_event import CanonicalEvent
from scm_ontology.command_lifecycle import CommandLifecycle, CommandState
from scm_ontology.decision_authorization import AuthorizedDecision
from scm_ontology.execution_command import build_execution_command
from scm_ontology.execution_outcome_contract import build_execution_outcome_contract
from scm_ontology.external_execution_adapter import ReferenceExternalExecutionAdapter
from scm_ontology.outcome_to_event_canonicalization import (
    OutcomeCanonicalizationError,
    canonicalize_execution_outcome,
    extract_outcome_canonical_lineage,
)
from scm_ontology.proposal_validation import ValidatedDecisionProposal
from scm_ontology.reasoning_output import ReasoningOutput


def command(proposal=None):
    output = ReasoningOutput(
        context_id="ctx-1",
        proposal=proposal or {"action": "replenish"},
        rationale="stock is below threshold",
        evidence_ids=("e1", "e2"),
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


def governed_result(proposal=None):
    return approve_and_execute(
        command(proposal),
        adapter=ReferenceExternalExecutionAdapter(),
        executed_at="2026-08-19T01:00:00Z",
        actor_id="planner-1",
    )


def test_outcome_canonicalizes_to_governed_canonical_event():
    event = canonicalize_execution_outcome(governed_result())
    assert isinstance(event, CanonicalEvent)
    assert event.event_type == "execution_outcome_recorded"
    assert event.entity_id == "cmd-1"
    assert event.occurred_at.isoformat() == "2026-08-19T01:00:00+00:00"
    attrs = dict(event.attributes)
    assert attrs["verdict"] == "success"
    assert attrs["governance_state"] == "executed"
    assert attrs["governance_command_id"] == "cmd-1"
    assert attrs["evidence_ids"] == ["e1", "e2"]
    assert attrs["provenance_ids"] == ["p1"]


def test_canonical_event_embeds_governance_actor_chain():
    event = canonicalize_execution_outcome(governed_result())
    attrs = dict(event.attributes)
    assert "planner-1" in attrs["governance_actors"]


def test_event_occurred_at_can_be_overridden():
    event = canonicalize_execution_outcome(
        governed_result(), event_occurred_at="2026-08-19T02:00:00Z"
    )
    assert event.occurred_at.isoformat() == "2026-08-19T02:00:00+00:00"


def test_fail_closed_when_not_governed():
    # A raw outcome contract (no governed approval-to-execution result) is refused.
    outcome = build_execution_outcome_contract(
        command(),
        elements=(),
        recorded_at="2026-08-19T01:00:00Z",
        verdict="rejected",
    )
    with pytest.raises(OutcomeCanonicalizationError):
        canonicalize_execution_outcome(outcome)  # type: ignore[arg-type]


def test_fail_closed_when_lifecycle_not_executed():
    from scm_ontology.command_lifecycle import start_command_lifecycle

    lifecycle = start_command_lifecycle("cmd-1")
    # Build a fake result whose lifecycle is NOT at executed by direct construct.
    from scm_ontology.approval_to_execution_runtime import ApprovalToExecutionResult
    from scm_ontology.external_execution_adapter import InMemoryExternalSystem

    # Use a partial flow: build a governed result, then engineer a non-terminal lifecycle.
    result = governed_result()
    bad = ApprovalToExecutionResult(
        lifecycle=lifecycle,
        outcome=result.outcome,
        dry_run=result.dry_run,
        executed_at=result.executed_at,
    )
    with pytest.raises(OutcomeCanonicalizationError):
        canonicalize_execution_outcome(bad)


def test_lineage_extraction():
    event = canonicalize_execution_outcome(governed_result())
    lineage = extract_outcome_canonical_lineage(event)
    assert lineage["event_id"] == "cmd-1"
    assert lineage["evidence_ids"] == ["e1", "e2"]
    assert lineage["provenance_ids"] == ["p1"]
