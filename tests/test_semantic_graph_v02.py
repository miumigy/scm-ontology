from scm_ontology.semantic_graph_v02 import (
    CANONICAL_SEMANTIC_LAYERS,
    validate_semantic_graph_v02,
)


def test_v02_contains_required_semantic_layers():
    assert CANONICAL_SEMANTIC_LAYERS == (
        "entity",
        "relationship",
        "transaction",
        "planning",
        "physical_flow",
        "event",
        "state",
        "temporal",
    )


def test_main_ontology_is_consistent_with_v02_contract():
    assert validate_semantic_graph_v02() == []
