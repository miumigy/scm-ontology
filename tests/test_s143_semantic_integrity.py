from scm_ontology.canonical_model import (
    CANONICAL_CONCEPTS,
    CANONICAL_RELATIONSHIPS,
    ConceptLayer,
    get_concept,
    relationship_predicates,
)


def test_closed_loop_concepts_are_registered() -> None:
    names = {concept.name for concept in CANONICAL_CONCEPTS}
    required = {
        "Recommendation",
        "Decision",
        "Action",
        "Execution",
        "Outcome",
        "Measurement",
        "PerformanceAssessment",
        "LearningResult",
    }
    assert required <= names


def test_action_is_not_described_as_execution() -> None:
    action = get_concept("Action")
    execution = get_concept("Execution")
    assert "not the execution record" in action.description
    assert "Record of carrying out" in execution.description


def test_derived_concepts_remain_derived() -> None:
    assert get_concept("KPI").layer is ConceptLayer.DERIVED
    assert get_concept("PerformanceAssessment").layer is ConceptLayer.DERIVED
    assert get_concept("Variance").layer is ConceptLayer.DERIVED
    assert get_concept("RiskScore").layer is ConceptLayer.DERIVED


def test_core_lifecycle_relations_exist() -> None:
    predicates = relationship_predicates()
    assert {
        "informs",
        "authorized_by",
        "execution_of",
        "executed_by",
        "results_in",
        "learns_from",
        "updates",
    } <= predicates


def test_relationship_endpoints_are_registered() -> None:
    names = {concept.name for concept in CANONICAL_CONCEPTS}
    assert all(
        relationship.source in names and relationship.target in names
        for relationship in CANONICAL_RELATIONSHIPS
    )
