from scm_ontology.canonical_model import (
    CANONICAL_CONCEPTS,
    CANONICAL_RELATIONSHIPS,
    ConceptLayer,
    concept_names,
)
from scm_ontology.model_integrity import audit_canonical_model, assert_canonical_model_integrity


def test_canonical_model_passes_integrity_audit() -> None:
    assert_canonical_model_integrity()
    assert audit_canonical_model() == ()


def test_concept_names_are_unique() -> None:
    names = [concept.name for concept in CANONICAL_CONCEPTS]
    assert len(names) == len(set(names))


def test_relationship_predicates_are_unique() -> None:
    predicates = [relation.predicate for relation in CANONICAL_RELATIONSHIPS]
    assert len(predicates) == len(set(predicates))


def test_relationship_endpoints_resolve() -> None:
    names = concept_names()
    for relation in CANONICAL_RELATIONSHIPS:
        assert relation.source in names
        assert relation.target in names


def test_derived_metrics_remain_derived() -> None:
    concepts = {concept.name: concept for concept in CANONICAL_CONCEPTS}
    for name in ("KPI", "PerformanceAssessment", "Variance", "RiskScore"):
        assert concepts[name].layer is ConceptLayer.DERIVED


def test_execution_lifecycle_is_explicit() -> None:
    predicates = {relation.predicate for relation in CANONICAL_RELATIONSHIPS}
    assert {"informs", "authorized_by", "execution_of", "results_in"} <= predicates


def test_learning_loop_is_explicit() -> None:
    predicates = {relation.predicate for relation in CANONICAL_RELATIONSHIPS}
    assert {"learns_from", "updates", "supersedes"} <= predicates
