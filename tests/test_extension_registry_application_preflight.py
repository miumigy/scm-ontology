from scm_ontology.extension_governance_decision import GovernanceDecision
from scm_ontology.extension_proposal import build_extension_proposal
from scm_ontology.extension_registry_application import plan_registry_application
from scm_ontology.extension_registry_application_gate import validate_registry_application_gate
from scm_ontology.extension_registry_application_preflight import run_registry_application_preflight


def test_preflight_marks_validated_gate_ready_without_mutation() -> None:
    proposal = build_extension_proposal(
        "candidate:1", "supports", "Order", "Product", GovernanceDecision.ACCEPTED
    )
    plan = plan_registry_application(proposal)
    gate = validate_registry_application_gate(plan)
    preflight = run_registry_application_preflight(gate)
    assert preflight.gate is gate
    assert preflight.ready is True
