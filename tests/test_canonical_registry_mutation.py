import pytest

from scm_ontology.canonical_relations import CANONICAL_RELATION_TYPES, RelationKind
from scm_ontology.extension_governance_decision import GovernanceDecision
from scm_ontology.extension_proposal import build_extension_proposal
from scm_ontology.extension_registry_application import plan_registry_application
from scm_ontology.extension_registry_application_gate import validate_registry_application_gate
from scm_ontology.extension_registry_application_preflight import run_registry_application_preflight
from scm_ontology.registry_mutation_guard import build_registry_mutation_guard
from scm_ontology.canonical_registry_mutation import (
    CanonicalRegistryMutationError,
    apply_canonical_registry_mutation,
)


def _guard(predicate_ref: str = "supports", inverse_ref: str | None = "supported_by"):
    proposal = build_extension_proposal(
        "candidate:1", predicate_ref, "Order", "Product", GovernanceDecision.ACCEPTED
    )
    preflight = run_registry_application_preflight(
        validate_registry_application_gate(plan_registry_application(proposal))
    )
    refs = frozenset({"supports", "supported_by"})
    return build_registry_mutation_guard(
        preflight,
        predicate_refs=refs,
        inverse_refs=frozenset({inverse_ref}) if inverse_ref else frozenset(),
    )


def test_accepted_proposal_is_functionally_applied() -> None:
    registry = CANONICAL_RELATION_TYPES
    result = apply_canonical_registry_mutation(
        _guard(), registry, kind=RelationKind.OPERATIONAL, inverse_ref="supported_by"
    )
    assert len(result.registry) == len(registry) + 1
    assert result.registry[-1].predicate_ref == "supports"
    assert len(registry) == len(CANONICAL_RELATION_TYPES)


def test_existing_predicate_is_rejected() -> None:
    with pytest.raises(CanonicalRegistryMutationError):
        apply_canonical_registry_mutation(
            _guard("causes", "caused_by"),
            CANONICAL_RELATION_TYPES,
            kind=RelationKind.CAUSAL,
            inverse_ref="caused_by",
        )
