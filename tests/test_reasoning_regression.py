from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.evidence_aggregation import aggregate_evidence
from scm_ontology.evidence_provenance import EvidenceRef, EvidenceSet
from scm_ontology.multi_hop_reasoning import MultiHopReasoningRequest, reason_over_paths
from scm_ontology.path_constraints import PathContainsNode
from scm_ontology.path_evidence import PathEvidence
from scm_ontology.path_reasoning_result import PathReasoningResult
from scm_ontology.reasoning_confidence import ConfidenceFactors, calculate_reasoning_confidence
from scm_ontology.reasoning_explanation import explain_path_reasoning
from scm_ontology.relation_path_query import RelationPathQuery, query_relation_paths
from scm_ontology.relationship_identity import RelationshipInstance


def graph() -> CanonicalGraph:
    return CanonicalGraph(
        nodes=(SemanticNode("product:1", "Product"), SemanticNode("supplier:1", "Supplier"), SemanticNode("site:1", "Site")),
        relationships=(
            CanonicalRelationship(RelationshipInstance("rel:1", "product:1", "supplies", "supplier:1")),
            CanonicalRelationship(RelationshipInstance("rel:2", "supplier:1", "located_at", "site:1")),
        ),
    )


def test_end_to_end_reasoning_contract_is_stable() -> None:
    result = reason_over_paths(graph(), MultiHopReasoningRequest(RelationPathQuery("product:1", ("supplies", "located_at")), "site:1", ("erp:1",)))
    assert result.status == "matched"
    explanation = explain_path_reasoning(result)
    assert tuple(step.ref for step in explanation.steps) == ("rel:1", "rel:2", "erp:1")
    confidence = calculate_reasoning_confidence(ConfidenceFactors(1.0, 1.0, 1.0, 1.0))
    assert confidence.score == 1.0


def test_path_query_and_constraint_remain_read_only_and_composable() -> None:
    matches = query_relation_paths(graph(), RelationPathQuery("product:1", ("supplies", "located_at")))
    filtered = tuple(match for match in matches if "supplier:1" in match.node_ids)
    assert len(filtered) == 1
    assert filtered[0].relationship_ids == ("rel:1", "rel:2")


def test_evidence_aggregation_is_deterministic() -> None:
    aggregated = aggregate_evidence(EvidenceSet((EvidenceRef("erp:1"),)), EvidenceSet((EvidenceRef("wms:1"), EvidenceRef("erp:1"))))
    assert tuple(ref.source_ref for ref in aggregated.evidence.refs) == ("erp:1", "wms:1")
