import pytest

from scm_ontology.extension_governance_decision import GovernanceDecision
from scm_ontology.extension_proposal import InvalidExtensionProposal, build_extension_proposal


def test_accepted_decision_builds_extension_proposal() -> None:
    proposal = build_extension_proposal(
        "candidate:1", "supports", "Order", "Product", GovernanceDecision.ACCEPTED
    )
    assert proposal.candidate_ref == "candidate:1"
    assert proposal.predicate_ref == "supports"


def test_pending_decision_cannot_build_extension_proposal() -> None:
    with pytest.raises(InvalidExtensionProposal):
        build_extension_proposal(
            "candidate:1", "supports", "Order", "Product", GovernanceDecision.PENDING
        )
