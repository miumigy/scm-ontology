import pytest

from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.canonical_graph_query import query_canonical_nodes, query_canonical_relationships
from scm_ontology.graph_query import GraphQueryError
from scm_ontology.relationship_identity import RelationshipInstance


def graph() -> CanonicalGraph:
    a = SemanticNode("a", "Location", {"name": "東京"})
    b = SemanticNode("b", "Location", {"name": "大阪"})
    rel = CanonicalRelationship(RelationshipInstance("r1", "a", "LANE", "b"))
    return CanonicalGraph(nodes=(b, a), relationships=(rel,))


def test_query_canonical_nodes_is_exact_and_deterministic():
    result = query_canonical_nodes(graph(), node_type="Location")
    assert [node.node_id for node in result.nodes] == ["a", "b"]
    assert [rel.relationship_id for rel in result.relationships] == ["r1"]


def test_query_canonical_relationships_by_endpoint():
    result = query_canonical_relationships(graph(), node_id="a")
    assert [rel.relationship_id for rel in result.relationships] == ["r1"]
    assert [node.node_id for node in result.nodes] == ["a", "b"]


def test_query_canonical_relationships_by_predicate():
    result = query_canonical_relationships(graph(), relationship_type="LANE")
    assert [rel.relationship_id for rel in result.relationships] == ["r1"]


def test_query_rejects_blank_filters():
    with pytest.raises(GraphQueryError):
        query_canonical_nodes(graph(), node_id=" ")
    with pytest.raises(GraphQueryError):
        query_canonical_relationships(graph(), relationship_type="")
