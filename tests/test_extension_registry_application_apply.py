from scm_ontology.extension_governance_decision import GovernanceDecision
from scm_ontology.extension_proposal import build_extension_proposal
from scm_ontology.extension_registry_application import apply_registry_application, plan_registry_application
from scm_ontology.extension_registry_application_gate import validate_registry_application_gate
from scm_ontology.extension_registry_application_preflight import run_registry_application_preflight


def test_ready_preflight_creates_application_intent_without_mutation() -> None:
    proposal = build_extension_proposal(
        "candidate:1", "supports", "Order", "Product", GovernanceDecision.ACCEPTED
    )
    plan = plan_registry_application(proposal)
    gate = validate_registry_application_gate(plan)
    preflight = run_registry_application_preflight(gate)
    intent = apply_registry_application(preflight)
    assert intent.preflight is preflight
