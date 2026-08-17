import pytest

from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.canonical_graph_persistence import InMemoryCanonicalGraphStore
from scm_ontology.canonical_graph_query import CanonicalGraphQueryBoundary, CanonicalGraphQueryError
from scm_ontology.relationship_identity import RelationshipInstance


def graph(node_prefix: str = "") -> CanonicalGraph:
    return CanonicalGraph(
        nodes=(
            SemanticNode(f"b{node_prefix}", "Location", {"name": "B"}),
            SemanticNode(f"a{node_prefix}", "Warehouse", {"name": "A"}),
        ),
        relationships=(
            CanonicalRelationship(RelationshipInstance(f"r2{node_prefix}", f"a{node_prefix}", "ships_to", f"b{node_prefix}")),
            CanonicalRelationship(RelationshipInstance(f"r1{node_prefix}", f"b{node_prefix}", "located_at", f"a{node_prefix}")),
        ),
    )


def test_query_is_version_aware_and_deterministic():
    store = InMemoryCanonicalGraphStore()
    store.save("g1", graph(), graph_version="1")
    store.save("g1", graph("v2"), graph_version="2")
    query = CanonicalGraphQueryBoundary(store)

    result = query.nodes("g1", graph_version="1")
    assert tuple(node.node_id for node in result.nodes) == ("a", "b")
    assert tuple(rel.relationship_id for rel in result.relationships) == ("r1", "r2")


def test_query_filters_nodes_and_relationships():
    store = InMemoryCanonicalGraphStore()
    store.save("g1", graph())
    query = CanonicalGraphQueryBoundary(store)

    nodes = query.nodes("g1", node_type="Warehouse")
    assert tuple(node.node_id for node in nodes.nodes) == ("a",)
    assert tuple(rel.relationship_id for rel in nodes.relationships) == ("r2",)

    relationships = query.relationships("g1", relationship_type="located_at", node_id="b")
    assert tuple(rel.relationship_id for rel in relationships.relationships) == ("r1",)
    assert tuple(node.node_id for node in relationships.nodes) == ("a", "b")


def test_query_results_are_immutable_and_missing_graph_fails_closed():
    store = InMemoryCanonicalGraphStore()
    store.save("g1", graph())
    query = CanonicalGraphQueryBoundary(store)
    result = query.nodes("g1")
    with pytest.raises(TypeError):
        result.nodes[0] = result.nodes[0]
    with pytest.raises(CanonicalGraphQueryError, match="graph_id not found"):
        query.nodes("missing")


def test_query_rejects_blank_filters():
    store = InMemoryCanonicalGraphStore()
    store.save("g1", graph())
    query = CanonicalGraphQueryBoundary(store)
    with pytest.raises(CanonicalGraphQueryError, match="node_type must be non-empty"):
        query.nodes("g1", node_type=" ")
