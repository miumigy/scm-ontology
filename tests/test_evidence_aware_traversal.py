from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.evidence_aware_traversal import (
    EvidenceAwareTraversalRequest,
    EvidenceMissing,
    evidence_aware_traversal_to_mapping,
    execute_evidence_aware_traversal,
)
from scm_ontology.relationship_identity import RelationshipInstance
from scm_ontology.relationship_version import RelationshipVersion
from scm_ontology.temporal_semantic_query import TemporalSemanticQueryRequest


def graph() -> CanonicalGraph:
    nodes = tuple(SemanticNode(node_id=value, node_type="Site") for value in ("A", "B", "C"))
    relationships = (
        CanonicalRelationship(
            RelationshipInstance("r-ab", "A", "ships", "B"),
            (RelationshipVersion("2026-01-01T00:00:00+00:00", qualifiers={"lead_time_days": 2}),),
        ),
        CanonicalRelationship(
            RelationshipInstance("r-bc", "B", "ships", "C"),
            (RelationshipVersion("2026-01-01T00:00:00+00:00", qualifiers={"lead_time_days": 3}),),
        ),
    )
    return CanonicalGraph(nodes, relationships)


def request(require_evidence: bool = True) -> EvidenceAwareTraversalRequest:
    return EvidenceAwareTraversalRequest(
        TemporalSemanticQueryRequest(
            "2026-06-01T00:00:00+00:00", "A", "C", predicates=("ships",), max_hops=4
        ),
        require_evidence=require_evidence,
    )


def test_traversal_attaches_evidence_to_every_step() -> None:
    result = execute_evidence_aware_traversal(
        graph(), request(), evidence_ids_by_relationship_id={"r-ab": ("ev-ab",), "r-bc": ("ev-bc",)}
    )

    assert result.status == "resolved"
    assert result.paths[0].node_ids == ("A", "B", "C")
    assert result.paths[0].steps[0].evidence_ids == ("ev-ab",)
    assert result.paths[0].steps[1].evidence_ids == ("ev-bc",)

    payload = evidence_aware_traversal_to_mapping(result)
    assert payload["paths"][0]["steps"][1]["evidence_ids"] == ["ev-bc"]


def test_required_evidence_fails_closed() -> None:
    try:
        execute_evidence_aware_traversal(
            graph(), request(), evidence_ids_by_relationship_id={"r-ab": ("ev-ab",)}
        )
    except EvidenceMissing as exc:
        assert str(exc) == "r-bc"
    else:
        raise AssertionError("expected EvidenceMissing")


def test_optional_evidence_preserves_unprovenanced_step_without_mutation() -> None:
    source = graph()
    before = source.to_json()
    result = execute_evidence_aware_traversal(
        source, request(False), evidence_ids_by_relationship_id={"r-ab": "ev-ab"}
    )

    assert result.paths[0].steps[0].evidence_ids == ("ev-ab",)
    assert result.paths[0].steps[1].evidence_ids == ()
    assert source.to_json() == before
