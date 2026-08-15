import pytest

from scm_ontology.canonical_graph import CanonicalGraph, SemanticNode
from scm_ontology.reasoning_query import NodeQuery
from scm_ontology.semantic_constraints import (
    PropertyEquals,
    SemanticConstraintError,
    evaluate_property_equals,
)


def test_property_equals_evaluates_only_selected_canonical_nodes() -> None:
    graph = CanonicalGraph(
        nodes=(
            SemanticNode("product:1", "Product", {"status": "active"}),
            SemanticNode("product:2", "Product", {"status": "inactive"}),
            SemanticNode("site:1", "Site", {"status": "active"}),
        )
    )
    assert evaluate_property_equals(
        graph,
        NodeQuery(node_type="Product"),
        PropertyEquals("status", "active"),
    ) == ("product:1",)


def test_property_equals_requires_a_non_empty_key() -> None:
    graph = CanonicalGraph(nodes=(SemanticNode("product:1", "Product"),))
    with pytest.raises(SemanticConstraintError):
        evaluate_property_equals(graph, NodeQuery(node_id="product:1"), PropertyEquals("", "active"))
