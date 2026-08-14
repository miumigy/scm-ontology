from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.relationship_identity import RelationshipInstance
from scm_ontology.scm_graph import SCMGraph
from scm_ontology.semantic_query import SemanticQuery


def test_incoming_neighbors_are_supported() -> None:
    graph = SCMGraph(CanonicalGraph())
    graph = graph.add_node(SemanticNode("order-1", "Order"))
    graph = graph.add_node(SemanticNode("supplier-1", "Supplier"))
    graph = graph.add_relationship(CanonicalRelationship(RelationshipInstance("r1", "order-1", "supplied_by", "supplier-1")))
    result = SemanticQuery(graph).neighbors("supplier-1", direction="in")
    assert [match.node.node_id for match in result] == ["order-1"]
