from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.relationship_identity import RelationshipInstance
from scm_ontology.relationship_version import RelationshipVersion
from scm_ontology.temporal_semantic_query import (
    PROTOCOL_VERSION,
    TemporalSemanticQueryRequest,
    execute_temporal_semantic_query,
    temporal_semantic_query_to_mapping,
)


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


def request() -> TemporalSemanticQueryRequest:
    return TemporalSemanticQueryRequest(
        "2026-06-01T00:00:00+00:00", "A", "C", predicates=("ships",), max_hops=4
    )


def test_query_resolves_temporal_path_with_qualifiers_and_provenance() -> None:
    result = execute_temporal_semantic_query(graph(), request())

    assert result.contract_version == PROTOCOL_VERSION
    assert result.status == "resolved"
    assert result.paths[0].node_ids == ("A", "B", "C")
    assert result.paths[0].steps[0].qualifiers["lead_time_days"] == 2
    assert len(result.graph_digest) == 64

    payload = temporal_semantic_query_to_mapping(result)
    assert payload["paths"][0]["provenance"]["graph_digest"] == result.graph_digest
    assert payload["paths"][0]["provenance"]["relationship_ids"] == ["r-ab", "r-bc"]


def test_query_is_deterministic_and_read_only() -> None:
    source = graph()
    before = source.to_json()
    first = temporal_semantic_query_to_mapping(execute_temporal_semantic_query(source, request()))
    second = temporal_semantic_query_to_mapping(execute_temporal_semantic_query(source, request()))

    assert first == second
    assert source.to_json() == before


def test_query_fails_closed_when_no_temporal_path_exists() -> None:
    result = execute_temporal_semantic_query(
        graph(),
        TemporalSemanticQueryRequest("2025-06-01T00:00:00+00:00", "A", "C"),
    )

    assert result.status == "not_found"
    assert result.paths == ()


def test_predicates_are_explicit_and_canonicalized_by_request_contract() -> None:
    request_value = TemporalSemanticQueryRequest(
        "2026-06-01T00:00:00+00:00", "A", "C", predicates=("ships",)
    )
    result = execute_temporal_semantic_query(graph(), request_value)
    assert result.paths
