from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.relationship_identity import RelationshipInstance
from scm_ontology.scm_graph import SCMGraph, SCMGraphError, empty_scm_graph


def graph() -> SCMGraph:
    nodes = (
        SemanticNode("order-1", "CustomerOrder"),
        SemanticNode("supplier-a", "Party"),
    )
    relationship = CanonicalRelationship(
        RelationshipInstance("r1", "order-1", "supplied_by", "supplier-a")
    )
    return SCMGraph(CanonicalGraph(nodes, (relationship,)))


def test_add_nodes_and_relationship_and_lookup():
    scm = empty_scm_graph().add_node(SemanticNode("a", "Party")).add_node(SemanticNode("b", "Party"))
    rel = CanonicalRelationship(RelationshipInstance("r1", "a", "related_to", "b"))
    scm = scm.add_relationship(rel)
    assert scm.node("a").node_type == "Party"
    assert scm.relationship("r1") == rel


def test_relationship_requires_existing_endpoints():
    scm = empty_scm_graph().add_node(SemanticNode("a", "Party"))
    rel = CanonicalRelationship(RelationshipInstance("r1", "a", "related_to", "missing"))
    try:
        scm.add_relationship(rel)
    except SCMGraphError as exc:
        assert "unknown to node" in str(exc)
    else:
        raise AssertionError("expected unknown endpoint error")


def test_traversal_filters_predicate_and_direction():
    scm = graph()
    assert tuple(node.node_id for node in scm.related("order-1", predicate="supplied_by")) == ("supplier-a",)
    assert tuple(node.node_id for node in scm.related("supplier-a", direction="in")) == ("order-1",)
    assert scm.relationships_from("order-1", predicate="supplied_by")[0].instance.relationship_id == "r1"


def test_canonical_graph_and_json_are_preserved():
    scm = graph()
    assert scm.to_canonical().nodes[0].node_id == "order-1"
    assert '"predicate":"supplied_by"' in scm.to_json()


def test_duplicate_ids_are_rejected():
    scm = empty_scm_graph().add_node(SemanticNode("a", "Party"))
    try:
        scm.add_node(SemanticNode("a", "Party"))
    except SCMGraphError:
        pass
    else:
        raise AssertionError("expected duplicate node error")
