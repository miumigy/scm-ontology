import pytest

from scm_ontology.extension_governance_decision import GovernanceDecision
from scm_ontology.extension_proposal import build_extension_proposal
from scm_ontology.extension_registry_application import plan_registry_application
from scm_ontology.extension_registry_application_gate import validate_registry_application_gate
from scm_ontology.extension_registry_application_preflight import run_registry_application_preflight
from scm_ontology.registry_mutation_guard import (
    RegistryMutationGuardError,
    build_registry_mutation_guard,
)


def _preflight():
    proposal = build_extension_proposal(
        "candidate:1", "supports", "Order", "Product", GovernanceDecision.ACCEPTED
    )
    return run_registry_application_preflight(
        validate_registry_application_gate(plan_registry_application(proposal))
    )


def test_guard_accepts_declared_inverse_refs() -> None:
    guard = build_registry_mutation_guard(
        _preflight(), predicate_refs=frozenset({"supports", "supported_by"}),
        inverse_refs=frozenset({"supported_by"}),
    )
    assert guard.predicate_refs == frozenset({"supports", "supported_by"})


def test_guard_rejects_undeclared_inverse_ref() -> None:
    with pytest.raises(RegistryMutationGuardError):
        build_registry_mutation_guard(
            _preflight(), predicate_refs=frozenset({"supports"}),
            inverse_refs=frozenset({"supported_by"}),
        )
