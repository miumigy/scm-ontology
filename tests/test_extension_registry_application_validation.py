import pytest

from scm_ontology.extension_proposal import ExtensionProposal
from scm_ontology.extension_registry_application import (
    InvalidRegistryApplicationPlan,
    plan_registry_application,
)


def test_valid_proposal_builds_plan() -> None:
    proposal = ExtensionProposal("candidate:1", "supports", "Order", "Product")
    plan = plan_registry_application(proposal)
    assert plan.proposal is proposal


def test_missing_candidate_is_rejected() -> None:
    with pytest.raises(InvalidRegistryApplicationPlan):
        plan_registry_application(ExtensionProposal("", "supports", "Order", "Product"))


def test_missing_endpoint_type_is_rejected() -> None:
    with pytest.raises(InvalidRegistryApplicationPlan):
        plan_registry_application(ExtensionProposal("candidate:1", "supports", "", "Product"))
