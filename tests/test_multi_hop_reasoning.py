from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.multi_hop_reasoning import MultiHopReasoningRequest, reason_over_paths
from scm_ontology.relation_path_query import RelationPathQuery
from scm_ontology.relationship_identity import RelationshipInstance


def graph() -> CanonicalGraph:
    return CanonicalGraph(
        nodes=(
            SemanticNode("product:1", "Product"),
            SemanticNode("supplier:1", "Supplier"),
            SemanticNode("site:1", "Site"),
        ),
        relationships=(
            CanonicalRelationship(RelationshipInstance("rel:1", "product:1", "supplies", "supplier:1")),
            CanonicalRelationship(RelationshipInstance("rel:2", "supplier:1", "located_at", "site:1")),
        ),
    )


def test_multi_hop_reasoning_composes_path_constraint_and_evidence() -> None:
    result = reason_over_paths(
        graph(),
        MultiHopReasoningRequest(
            RelationPathQuery("product:1", ("supplies", "located_at")),
            end_node_id="site:1",
            source_refs=("erp:order:1", "wms:stock:2"),
        ),
    )
    assert result.status == "matched"
    assert len(result.paths) == 1
    assert result.paths[0].path.node_ids == ("product:1", "supplier:1", "site:1")
    assert tuple(ref.source_ref for ref in result.paths[0].evidence.refs) == ("erp:order:1", "wms:stock:2")


def test_multi_hop_reasoning_returns_no_match_for_unsatisfied_endpoint() -> None:
    result = reason_over_paths(
        graph(),
        MultiHopReasoningRequest(
            RelationPathQuery("product:1", ("supplies", "located_at")),
            end_node_id="site:missing",
        ),
    )
    assert result.status == "no_match"
    assert result.paths == ()
