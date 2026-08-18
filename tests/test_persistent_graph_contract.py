import json

import pytest

from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, CanonicalGraphError, SemanticNode
from scm_ontology.evidence_provenance import EvidenceRef
from scm_ontology.relationship_identity import RelationshipInstance
from scm_ontology.relationship_version import RelationshipVersion
from scm_ontology.persistent_graph_contract import (
    PersistentGraphContractError,
    PersistedElement,
    PersistedGraphDocument,
    document_from_mapping,
    element_by_id,
    persistence_element_id,
    persistent_graph_document,
)


def _graph() -> CanonicalGraph:
    return CanonicalGraph(
        nodes=(
            SemanticNode("supplier-1", "Supplier", {"name": "Acme"}),
            SemanticNode("factory-1", "Factory"),
        ),
        relationships=(
            CanonicalRelationship(
                RelationshipInstance("rel-1", "supplier-1", "supplies", "factory-1"),
                (RelationshipVersion("2026-01-01", "2026-12-31"),),
            ),
        ),
    )


def _provenance() -> dict[str, tuple[EvidenceRef, ...]]:
    return {
        persistence_element_id("node", "supplier-1"): (
            EvidenceRef("erp:SUP-1", observed_at="2026-08-19T09:00:00Z"),
        ),
        persistence_element_id("relationship", "rel-1"): (
            EvidenceRef("tms:assets-1"),
        ),
    }


def test_document_contains_all_element_kinds() -> None:
    graph = _graph()
    doc = persistent_graph_document(graph, scope="enterprise:acme")
    kinds = sorted({el.kind for el in doc.elements})
    assert kinds == ["node", "relationship", "relationship_version"]
    assert len(doc.elements) == 4  # 2 nodes + 1 relationship + 1 version


def test_document_is_deterministic_and_content_addressed() -> None:
    graph = _graph()
    d1 = persistent_graph_document(graph, scope="enterprise:acme")
    d2 = persistent_graph_document(graph, scope="enterprise:acme")
    assert d1.document_digest == d2.document_digest
    assert d1.to_json() == d2.to_json()
    # canonical digest anchors the source graph
    assert d1.canonical_digest != ""
    # changing scope changes the document identity
    d3 = persistent_graph_document(graph, scope="enterprise:other")
    assert d3.document_digest != d1.document_digest


def test_node_relationship_version_temporal_encoding() -> None:
    graph = _graph()
    doc = persistent_graph_document(graph, scope="enterprise:acme")
    version = element_by_id(doc, persistence_element_id("relationship_version", "rel-1#v:2026-01-01"))
    assert version is not None
    assert version.kind == "relationship_version"
    assert version.effective_at == "2026-01-01"
    assert version.valid_to == "2026-12-31"
    assert version.payload["relationship_id"] == "rel-1"


def test_provenance_attachment_is_preserved() -> None:
    graph = _graph()
    doc = persistent_graph_document(graph, scope="enterprise:acme", provenance=_provenance())
    node = element_by_id(doc, persistence_element_id("node", "supplier-1"))
    assert node is not None
    assert len(node.provenance) == 1
    assert node.provenance[0].source_ref == "erp:SUP-1"
    rel = element_by_id(doc, persistence_element_id("relationship", "rel-1"))
    assert rel is not None
    assert rel.provenance[0].source_ref == "tms:assets-1"


def test_roundtrip_mapping_preserves_all_semantics() -> None:
    graph = _graph()
    doc = persistent_graph_document(graph, scope="enterprise:acme", provenance=_provenance())
    restored = document_from_mapping(json.loads(doc.to_json()))
    assert restored.document_digest == doc.document_digest
    assert restored.to_json() == doc.to_json()


def test_document_from_mapping_fails_closed_on_digest_mismatch() -> None:
    graph = _graph()
    doc = persistent_graph_document(graph, scope="enterprise:acme")
    mapping = json.loads(doc.to_json())
    mapping["document_digest"] = "0" * 64
    with pytest.raises(PersistentGraphContractError, match="digest mismatch"):
        document_from_mapping(mapping)


def test_fail_closed_on_empty_scope() -> None:
    with pytest.raises(PersistentGraphContractError, match="scope"):
        persistent_graph_document(_graph(), scope="   ")


def test_fail_closed_on_dangling_relationship_endpoint() -> None:
    graph = CanonicalGraph(
        nodes=(SemanticNode("only-1", "Supplier"),),
        relationships=(
            CanonicalRelationship(RelationshipInstance("rel-9", "only-1", "ships_to", "missing-1")),
        ),
    )
    with pytest.raises(PersistentGraphContractError, match="not present in the graph"):
        persistent_graph_document(graph, scope="enterprise:acme")


def test_element_requires_identity() -> None:
    with pytest.raises(PersistentGraphContractError, match="element identity"):
        persistence_element_id("node", "  ")


def test_unsupported_element_kind_rejected() -> None:
    with pytest.raises(PersistentGraphContractError, match="persistence element kind"):
        PersistedElement(kind="edge", element_id="x", payload={})
    with pytest.raises(PersistentGraphContractError, match="persistence element kind"):
        persistence_element_id("edge", "x")


def test_document_is_immutable() -> None:
    graph = _graph()
    doc = persistent_graph_document(graph, scope="enterprise:acme")
    with pytest.raises(Exception):
        doc.elements = ()  # type: ignore[assignment]
    with pytest.raises(Exception):
        doc.canonical_digest = "x"  # type: ignore[assignment]
