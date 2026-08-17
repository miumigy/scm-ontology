from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.decision_runtime import MockReasoningProvider, run_decision_loop
from scm_ontology.execution_runtime import execute_dry_run
from scm_ontology.governed_audit import (
    DecisionGovernanceError,
    GovernedDecisionAuditEntry,
    build_audit_trail,
    record_governed_decision,
    replay_governed_decision,
)
from scm_ontology.graph_reasoning_projection import GraphReasoningObservation


def run_result():
    observation = GraphReasoningObservation(
        question_id="warehouse-stock",
        value={"warehouse": "WH-1", "stock": 5, "threshold": 10},
        evidence_ids=("e-stock-1",),
        provenance_ids=("p-erp-1",),
    )
    return run_decision_loop(
        context_id="ctx-r4-audit",
        observations=(observation,),
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
        command_id="cmd-r4-audit",
    )


def dry_run(result):
    return execute_dry_run(result.execution_command, dry_ran_at="2026-08-17T21:00:01Z")


def audit_entry():
    result = run_result()
    return record_governed_decision(result, recorded_at="2026-08-17T21:00:00Z", dry_run=dry_run(result))


def test_audit_entry_is_recorded_and_content_addressed():
    entry = audit_entry()
    assert entry.context_id == "ctx-r4-audit"
    assert entry.command_id == "cmd-r4-audit"
    assert isinstance(entry.audit_id, str) and len(entry.audit_id) == 64


def test_audit_entry_is_deterministic():
    a = audit_entry()
    b = audit_entry()
    assert a.audit_id == b.audit_id
    assert a.to_json() == b.to_json()
    assert a.to_mapping()["contract_version"] == "S354.1"


def test_audit_entry_is_immutable():
    entry = audit_entry()
    with pytest.raises(FrozenInstanceError):
        entry.audit_id = "changed"


def test_audit_trail_bundles_entries():
    entry = audit_entry()
    trail = build_audit_trail([entry, entry])
    assert len(trail.entries) == 2
    assert trail.to_mapping()["contract_version"] == "S354.2"
    assert trail.to_mapping()["entry_count"] == 2


def test_audit_trail_rejects_empty():
    with pytest.raises(DecisionGovernanceError, match="audit trail must not be empty"):
        build_audit_trail([])


def test_record_rejects_invalid_input():
    with pytest.raises(DecisionGovernanceError, match="must be a DecisionRuntimeResult"):
        record_governed_decision(object(), recorded_at="t")
    result = run_result()
    with pytest.raises(DecisionGovernanceError, match="recorded_at must be non-empty"):
        record_governed_decision(result, recorded_at="  ")


def test_replay_reproduces_recorded_decision():
    entry = audit_entry()
    replayed = replay_governed_decision(
        entry,
        actor_id="planner-1",
        authority="supply-chain-manager",
        authorized_at="2026-08-17T21:00:00Z",
        command_type="replenishment",
        command_id="cmd-r4-audit",
    )
    assert replayed.to_mapping() == entry.result.authorized_decision.to_mapping()


def test_replay_fails_closed_on_content_drift():
    entry = audit_entry()
    # Tamper with the recorded proposal so the digest mismatch is detected.
    tampered = entry.result
    object.__setattr__(tampered.validated_proposal.output, "proposal", {"action": "stop"})
    with pytest.raises(DecisionGovernanceError, match="digest mismatch"):
        replay_governed_decision(
            entry,
            actor_id="planner-1",
            authority="supply-chain-manager",
            authorized_at="2026-08-17T21:00:00Z",
            command_type="replenishment",
            command_id="cmd-r4-audit",
        )
