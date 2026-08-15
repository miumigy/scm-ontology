from scm_ontology.extension_governance_decision import GovernanceDecision
from scm_ontology.extension_proposal import build_extension_proposal
from scm_ontology.extension_registry_application import plan_registry_application
from scm_ontology.extension_registry_application_gate import validate_registry_application_gate
from scm_ontology.extension_registry_application_preflight import run_registry_application_preflight
from scm_ontology.canonical_registry_application import apply_to_canonical_registry


def test_preflighted_application_crosses_explicit_boundary() -> None:
    proposal = build_extension_proposal(
        "candidate:1", "supports", "Order", "Product", GovernanceDecision.ACCEPTED
    )
    plan = plan_registry_application(proposal)
    gate = validate_registry_application_gate(plan)
    preflight = run_registry_application_preflight(gate)
    result = apply_to_canonical_registry(preflight)
    assert result.preflight is preflight
    assert result.applied is True
