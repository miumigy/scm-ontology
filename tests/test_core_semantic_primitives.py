from scm_ontology.core_semantic_primitives import CORE_SEMANTIC_PRIMITIVES, get_core_semantic_primitive


def test_registry_contains_expected_primitives():
    names = {p.name for p in CORE_SEMANTIC_PRIMITIVES}
    assert names == {
        "Entity", "MetricDefinition", "MetricObservation", "CanonicalState",
        "CanonicalEvent", "Impact", "Target", "Provenance", "Time",
    }


def test_registry_lookup_is_canonical():
    primitive = get_core_semantic_primitive("MetricObservation")
    assert primitive.kind == "observation"
    assert "State or Event" in primitive.non_goals[0]
