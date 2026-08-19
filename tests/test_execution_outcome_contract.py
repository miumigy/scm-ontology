from dataclasses import FrozenInstanceError

import pytest

from scm_ontology.decision_authorization import AuthorizedDecision
from scm_ontology.execution_command import build_execution_command
from scm_ontology.execution_outcome_contract import (
    ExecutionOutcomeContract,
    ExecutionOutcomeContractError,
    ResultElement,
    build_execution_outcome_contract,
    reject_execution_outcome_contract,
)
from scm_ontology.proposal_validation import ValidatedDecisionProposal
from scm_ontology.reasoning_output import ReasoningOutput


def command():
    output = ReasoningOutput(
        context_id="ctx-1",
        proposal="replenish",
        rationale="stock is below threshold",
        evidence_ids=("e-src-1",),
        provenance_ids=("p-src-1",),
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


def test_full_success_verdict():
    outcome = build_execution_outcome_contract(
        command(),
        elements=(
            ResultElement(
                target_ref="erp-po-1",
                status="success",
                external_reference="ERP-PO-1001",
            ),
        ),
        recorded_at="2026-08-19T01:00:00Z",
        evidence_ids=("e-1",),
        provenance_ids=("p-1",),
    )
    assert outcome.verdict == "success"
    assert outcome.command_id == "cmd-1"
    assert outcome.context_id == "ctx-1"
    assert outcome.to_mapping()["contract_version"] == "P9A.1"


def test_partial_verdict_deduced_from_mixed_elements():
    outcome = build_execution_outcome_contract(
        command(),
        elements=(
            ResultElement(target_ref="erp-po-1", status="success"),
            ResultElement(target_ref="erp-po-2", status="failure"),
        ),
        recorded_at="2026-08-19T01:00:00Z",
    )
    assert outcome.verdict == "partial"


def test_failure_verdict_when_all_failed():
    outcome = build_execution_outcome_contract(
        command(),
        elements=(
            ResultElement(target_ref="erp-po-1", status="failure"),
            ResultElement(target_ref="erp-po-2", status="failure"),
        ),
        recorded_at="2026-08-19T01:00:00Z",
    )
    assert outcome.verdict == "failure"


def test_rejected_outcome_has_no_elements():
    outcome = reject_execution_outcome_contract(
        command(),
        recorded_at="2026-08-19T01:00:00Z",
        detail="governance declined",
    )
    assert outcome.verdict == "rejected"
    assert outcome.elements == ()
    assert outcome.detail == "governance declined"


def test_outcome_id_is_deterministic():
    a = build_execution_outcome_contract(
        command(),
        elements=(ResultElement(target_ref="x", status="success"),),
        recorded_at="2026-08-19T01:00:00Z",
    )
    b = build_execution_outcome_contract(
        command(),
        elements=(ResultElement(target_ref="x", status="success"),),
        recorded_at="2026-08-19T01:00:00Z",
    )
    assert a.outcome_id == b.outcome_id
    assert a.to_json() == b.to_json()

    # Same recorded outcome content at a different recorded_at is content-addressed
    # to the same id (matching the governed-audit pattern, where the digest
    # excludes the wall-clock recorded_at so replay is reproducible).
    c = build_execution_outcome_contract(
        command(),
        elements=(ResultElement(target_ref="x", status="success"),),
        recorded_at="2026-08-19T02:00:00Z",
    )
    assert a.outcome_id == c.outcome_id

    # Changing the content (an element) changes the id.
    d = build_execution_outcome_contract(
        command(),
        elements=(ResultElement(target_ref="x", status="failure"),),
        recorded_at="2026-08-19T01:00:00Z",
    )
    assert a.outcome_id != d.outcome_id


def test_outcome_is_immutable():
    outcome = build_execution_outcome_contract(
        command(),
        elements=(ResultElement(target_ref="x", status="success"),),
        recorded_at="2026-08-19T01:00:00Z",
    )
    with pytest.raises(FrozenInstanceError):
        outcome.verdict = "failure"  # type: ignore[misc]


def test_inconsistent_verdict_fails_closed():
    with pytest.raises(ExecutionOutcomeContractError):
        build_execution_outcome_contract(
            command(),
            elements=(ResultElement(target_ref="x", status="success"),),
            recorded_at="2026-08-19T01:00:00Z",
            verdict="failure",
        )


def test_rejected_with_elements_fails_closed():
    with pytest.raises(ExecutionOutcomeContractError):
        build_execution_outcome_contract(
            command(),
            elements=(ResultElement(target_ref="x", status="success"),),
            recorded_at="2026-08-19T01:00:00Z",
            verdict="rejected",
        )


def test_invalid_element_status_rejected():
    with pytest.raises(ExecutionOutcomeContractError):
        ResultElement(target_ref="x", status="unknown")


def test_empty_elements_rejected_for_success_verdict():
    with pytest.raises(ExecutionOutcomeContractError):
        build_execution_outcome_contract(
            command(),
            elements=(),
            recorded_at="2026-08-19T01:00:00Z",
        )


def test_blank_evidence_id_rejected():
    with pytest.raises(ExecutionOutcomeContractError):
        build_execution_outcome_contract(
            command(),
            elements=(ResultElement(target_ref="x", status="success"),),
            recorded_at="2026-08-19T01:00:00Z",
            evidence_ids=(" ",),
        )
