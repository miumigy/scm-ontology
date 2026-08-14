from scm_ontology.cross_entity_validation import SemanticGraph, SemanticNode, validate_cross_entity
from scm_ontology.relationship_identity import RelationshipInstance


def node(node_id: str, node_type: str) -> SemanticNode:
    return SemanticNode(node_id, node_type)


def relationship(relationship_id: str = "R1") -> RelationshipInstance:
    return RelationshipInstance(relationship_id, "order-1", "places", "customer-1")


def test_resolved_relationship_is_valid():
    graph = SemanticGraph(
        nodes=(node("order-1", "CustomerOrder"), node("customer-1", "Customer")),
        relationships=(relationship(),),
    )

    result = validate_cross_entity(graph)

    assert result.valid
    assert result.issues == ()


def test_missing_endpoint_is_warning_not_error():
    graph = SemanticGraph(
        nodes=(node("order-1", "CustomerOrder"),),
        relationships=(relationship(),),
    )

    result = validate_cross_entity(graph)

    assert result.valid
    assert result.issues[0].code == "UNRESOLVED_ENDPOINT"


def test_same_node_id_with_conflicting_types_is_error():
    graph = SemanticGraph(
        nodes=(node("order-1", "CustomerOrder"), node("order-1", "Shipment")),
    )

    result = validate_cross_entity(graph)

    assert not result.valid
    assert result.issues[0].code == "ENTITY_TYPE_CONFLICT"


def test_same_relationship_id_with_conflicting_relationships_is_error():
    first = relationship("R1")
    second = RelationshipInstance("R1", "order-2", "places", "customer-1")
    graph = SemanticGraph(
        nodes=(node("order-1", "CustomerOrder"), node("order-2", "CustomerOrder"), node("customer-1", "Customer")),
        relationships=(first, second),
    )

    result = validate_cross_entity(graph)

    assert not result.valid
    assert result.issues[0].code == "RELATIONSHIP_IDENTITY_CONFLICT"


def test_domain_specific_relationships_remain_open_world():
    custom = RelationshipInstance("R2", "order-1", "custom_relation", "customer-1")
    graph = SemanticGraph(
        nodes=(node("order-1", "CustomerOrder"), node("customer-1", "Customer")),
        relationships=(custom,),
    )

    result = validate_cross_entity(graph)

    assert result.valid
