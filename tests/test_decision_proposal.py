import pytest

from scm_ontology.decision_proposal import (
    DecisionProposal,
    DecisionProposalError,
    decision_proposal_to_json,
)


def test_proposal_preserves_context_and_is_immutable() -> None:
    proposal = DecisionProposal(
        "D1", "expedite", "C1", {"item": "東京P"}, "supplier delay", evidence_ids=("E2", "E1"), provenance_ids=("P2", "P1"),
    )
    assert proposal.context_id == "C1"
    assert proposal.evidence_ids == ("E1", "E2")
    assert proposal.provenance_ids == ("P1", "P2")
    with pytest.raises(Exception):
        proposal.decision_id = "D2"


def test_empty_required_fields_fail_closed() -> None:
    with pytest.raises(DecisionProposalError):
        DecisionProposal("", "type", "C1", {}, "why")
    with pytest.raises(DecisionProposalError):
        DecisionProposal("D1", "", "C1", {}, "why")
    with pytest.raises(DecisionProposalError):
        DecisionProposal("D1", "type", "", {}, "why")
    with pytest.raises(DecisionProposalError):
        DecisionProposal("D1", "type", "C1", {}, "")


def test_json_is_deterministic_and_utf8_safe() -> None:
    proposal = DecisionProposal("D1", "replan", "C1", {"action": "再計画"}, "需要不足", evidence_ids=("証拠",))
    payload = decision_proposal_to_json(proposal)
    assert payload == decision_proposal_to_json(proposal)
    assert "再計画" in payload
    assert "証拠" in payload
    assert '"contract_version":"S334.1"' in payload
