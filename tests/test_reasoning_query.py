import pytest

from scm_ontology.canonical_graph import CanonicalGraph, SemanticNode
from scm_ontology.reasoning_query import NodeQuery, ReasoningQueryError, query_nodes


def test_query_nodes_filters_by_canonical_type_and_identity() -> None:
    graph = CanonicalGraph(
        nodes=(
            SemanticNode("product:1", "Product"),
            SemanticNode("site:1", "Site"),
            SemanticNode("product:2", "Product"),
        )
    )
    assert tuple(node.node_id for node in query_nodes(graph, NodeQuery(node_type="Product"))) == (
        "product:1",
        "product:2",
    )
    assert tuple(node.node_id for node in query_nodes(graph, NodeQuery(node_id="site:1"))) == ("site:1",)


def test_reasoning_query_requires_an_explicit_constraint() -> None:
    graph = CanonicalGraph(nodes=(SemanticNode("product:1", "Product"),))
    with pytest.raises(ReasoningQueryError):
        query_nodes(graph)
