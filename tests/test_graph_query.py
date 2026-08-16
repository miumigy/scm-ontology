import pytest

from scm_ontology.graph_projection import GraphNode, GraphProjection, GraphRelationship
from scm_ontology.graph_query import GraphQueryError, graph_query_to_json, query_nodes, query_relationships


def projection():
    a = GraphNode("a", "Location", (("name", "東京"),))
    b = GraphNode("b", "Location", (("name", "大阪"),))
    r = GraphRelationship("r1", "LANE", "a", "b")
    return GraphProjection((b, a), (r,), ("p2", "p1"))


def test_query_nodes_is_exact_and_deterministic():
    result = query_nodes(projection(), node_type="Location")
    assert [n.node_id for n in result.nodes] == ["a", "b"]
    assert result.provenance_ids == ("p1", "p2")
    assert "東京" in graph_query_to_json(result)


def test_query_relationships_by_endpoint():
    result = query_relationships(projection(), node_id="a")
    assert [r.relationship_id for r in result.relationships] == ["r1"]
    assert {n.node_id for n in result.nodes} == {"a", "b"}


def test_query_rejects_blank_filters():
    with pytest.raises(GraphQueryError):
        query_nodes(projection(), node_id=" ")
    with pytest.raises(GraphQueryError):
        query_relationships(projection(), relationship_type="")
