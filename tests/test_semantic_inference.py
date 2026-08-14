from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.relationship_identity import RelationshipInstance
from scm_ontology.scm_graph import SCMGraph
from scm_ontology.semantic_inference import InferenceRule, RelationshipPattern, infer


def graph() -> SCMGraph:
    canonical = CanonicalGraph(
        nodes=(
            SemanticNode("order-1", "Order"),
            SemanticNode("line-1", "OrderLine"),
            SemanticNode("product-1", "Product"),
        ),
        relationships=(
            CanonicalRelationship(
                RelationshipInstance("r1", "order-1", "contains", "line-1")
            ),
            CanonicalRelationship(
                RelationshipInstance("r2", "line-1", "references", "product-1")
            ),
        ),
    )
    return SCMGraph(canonical)


def test_two_hop_rule_derives_fact_with_provenance() -> None:
    rule = InferenceRule(
        "order-concerns-product",
        (
            RelationshipPattern("contains", "Order", "OrderLine"),
            RelationshipPattern("references", "OrderLine", "Product"),
        ),
        "concerns",
    )

    result = infer(graph(), rule)

    assert len(result) == 1
    assert result[0].from_id == "order-1"
    assert result[0].predicate == "concerns"
    assert result[0].to_id == "product-1"
    assert result[0].rule_id == "order-concerns-product"
    assert result[0].source_relationship_ids == ("r1", "r2")


def test_unknown_predicates_can_participate_in_open_world_inference() -> None:
    canonical = CanonicalGraph(
        nodes=(SemanticNode("a", "A"), SemanticNode("b", "B"), SemanticNode("c", "C")),
        relationships=(
            CanonicalRelationship(RelationshipInstance("r1", "a", "custom_link", "b")),
            CanonicalRelationship(RelationshipInstance("r2", "b", "custom_link_2", "c")),
        ),
    )
    rule = InferenceRule(
        "custom-chain",
        (RelationshipPattern("custom_link"), RelationshipPattern("custom_link_2")),
        "custom_derived",
    )

    result = infer(SCMGraph(canonical), rule)

    assert [(item.from_id, item.predicate, item.to_id) for item in result] == [
        ("a", "custom_derived", "c")
    ]


def test_inference_does_not_consume_its_own_output() -> None:
    rule = InferenceRule(
        "order-concerns-product",
        (
            RelationshipPattern("contains", "Order", "OrderLine"),
            RelationshipPattern("references", "OrderLine", "Product"),
        ),
        "concerns",
    )

    first = infer(graph(), rule)
    second = infer(graph(), rule)

    assert first == second
    assert all(item.predicate != "contains" for item in first)
