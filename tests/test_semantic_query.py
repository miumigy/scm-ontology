from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.relationship_identity import RelationshipInstance
from scm_ontology.scm_graph import SCMGraph
from scm_ontology.semantic_query import SemanticQuery


def graph() -> SCMGraph:
    base = SCMGraph(CanonicalGraph())
    base = base.add_node(SemanticNode("order-1", "Order"))
    base = base.add_node(SemanticNode("supplier-1", "Supplier"))
    base = base.add_node(SemanticNode("customer-1", "Customer"))
    base = base.add_relationship(
        CanonicalRelationship(
            RelationshipInstance("r1", "order-1", "supplied_by", "supplier-1")
        )
    )
    base = base.add_relationship(
        CanonicalRelationship(
            RelationshipInstance("r2", "order-1", "placed_by", "customer-1")
        )
    )
    return base


def test_nodes_can_filter_by_type() -> None:
    result = SemanticQuery(graph()).nodes(node_type="Supplier")
    assert [match.node.node_id for match in result] == ["supplier-1"]


def test_relationships_can_filter_by_predicate_and_endpoints() -> None:
    result = SemanticQuery(graph()).relationships(predicate="supplied_by", from_id="order-1")
    assert [match.relationship.instance.relationship_id for match in result] == ["r1"]


def test_neighbors_are_explicit_graph_facts() -> None:
    result = SemanticQuery(graph()).neighbors("order-1", predicate="supplied_by")
    assert [match.node.node_id for match in result] == ["supplier-1"]


def test_query_does_not_infer_unrepresented_supplier_capability() -> None:
    result = SemanticQuery(graph()).relationships(predicate="can_supply")
    assert result == ()


def test_fact_count_counts_nodes_and_relationships() -> None:
    assert SemanticQuery(graph()).fact_count() == 5
