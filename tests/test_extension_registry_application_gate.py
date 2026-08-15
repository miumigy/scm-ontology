from scm_ontology.extension_governance_decision import GovernanceDecision
from scm_ontology.extension_proposal import build_extension_proposal
from scm_ontology.extension_registry_application import plan_registry_application
from scm_ontology.extension_registry_application_gate import validate_registry_application_gate


def test_validated_plan_produces_application_gate() -> None:
    proposal = build_extension_proposal(
        "candidate:1", "supports", "Order", "Product", GovernanceDecision.ACCEPTED
    )
    plan = plan_registry_application(proposal)
    gate = validate_registry_application_gate(plan)
    assert gate.plan is plan
    assert gate.validated is True
