from scm_ontology.canonical_model import (
    CANONICAL_CONCEPTS,
    CANONICAL_RELATIONSHIPS,
    ConceptLayer,
    concepts_by_layer,
    concept_names,
    get_concept,
    relationship_predicates,
)


def test_concept_names_are_unique():
    assert len(concept_names()) == len(CANONICAL_CONCEPTS)


def test_relationship_predicates_are_unique():
    assert len(relationship_predicates()) == len(CANONICAL_RELATIONSHIPS)


def test_every_relationship_endpoint_is_declared():
    names = concept_names()
    for relation in CANONICAL_RELATIONSHIPS:
        assert relation.source in names
        assert relation.target in names


def test_core_excludes_derived_metrics():
    derived = {concept.name for concept in concepts_by_layer(ConceptLayer.DERIVED)}
    core = {concept.name for concept in concepts_by_layer(ConceptLayer.CORE)}
    assert {"KPI", "PerformanceAssessment", "Variance", "RiskScore"} <= derived
    assert not derived & core


def test_planned_and_actual_are_not_concepts():
    names = concept_names()
    assert "Actual" not in names
    assert "Planned" not in names


def test_epistemic_distinctions_are_not_collapsed():
    names = concept_names()
    assert {"Observation", "Event", "State"} <= names
    assert get_concept("Observation").layer == ConceptLayer.PRIMITIVE
    assert get_concept("Event").layer == ConceptLayer.PRIMITIVE
    assert get_concept("State").layer == ConceptLayer.PRIMITIVE


def test_causal_predicates_are_explicitly_categorized():
    causal = {r.predicate for r in CANONICAL_RELATIONSHIPS if r.category.value == "causal"}
    assert causal == {"causes", "affects"}
