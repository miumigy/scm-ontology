import pytest

from scm_ontology.extension_governance_decision import (
    ExtensionGovernanceDecision,
    GovernanceDecision,
    InvalidGovernanceTransition,
)


def test_pending_can_be_accepted() -> None:
    decision = ExtensionGovernanceDecision("candidate:1")
    assert decision.accept().status is GovernanceDecision.ACCEPTED
    assert decision.status is GovernanceDecision.PENDING


def test_pending_can_be_rejected() -> None:
    decision = ExtensionGovernanceDecision("candidate:1")
    assert decision.reject().status is GovernanceDecision.REJECTED


def test_final_decision_cannot_be_reapplied() -> None:
    accepted = ExtensionGovernanceDecision("candidate:1").accept()
    with pytest.raises(InvalidGovernanceTransition):
        accepted.reject()
