from scm_ontology.extension_governance_decision import GovernanceDecision
from scm_ontology.extension_proposal import build_extension_proposal
from scm_ontology.extension_registry_application import plan_registry_application


def test_registry_application_is_explicit_plan_only() -> None:
    proposal = build_extension_proposal(
        "candidate:1", "supports", "Order", "Product", GovernanceDecision.ACCEPTED
    )
    plan = plan_registry_application(proposal)
    assert plan.proposal is proposal
