import sqlite3

import pytest

from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.evidence_provenance import EvidenceRef
from scm_ontology.persistent_graph_contract import (
    PersistedGraphDocument,
    persistence_element_id,
    persistent_graph_document,
)
from scm_ontology.relationship_identity import RelationshipInstance
from scm_ontology.relationship_version import RelationshipVersion
from scm_ontology.relational_graph_backend import RelationalGraphBackend, RelationalGraphBackendError


def _graph() -> CanonicalGraph:
    return CanonicalGraph(
        nodes=(
            SemanticNode("supplier-1", "Supplier", {"name": "Acme", "risk": 2}),
            SemanticNode("factory-1", "Factory"),
            SemanticNode("dc-1", "DistributionCenter"),
        ),
        relationships=(
            CanonicalRelationship(
                RelationshipInstance("rel-1", "supplier-1", "supplies", "factory-1"),
                (RelationshipVersion("2026-01-01", "2026-12-31", {"commitment": "firm"}),),
            ),
            CanonicalRelationship(
                RelationshipInstance("rel-2", "factory-1", "ships_to", "dc-1")
            ),
        ),
    )


def _document(scope="enterprise:acme") -> PersistedGraphDocument:
    provenance = {
        persistence_element_id("node", "supplier-1"): (
            EvidenceRef("erp:SUP-1", observed_at="2026-08-19T09:00:00Z", metadata={"table": "suppliers"}),
        ),
        persistence_element_id("relationship", "rel-1"): (
            EvidenceRef("tms:assets-1"),
        ),
    }
    return persistent_graph_document(_graph(), scope=scope, provenance=provenance)


def _backend() -> RelationalGraphBackend:
    conn = sqlite3.connect(":memory:")
    return RelationalGraphBackend(conn)


def test_write_read_roundtrip_preserves_semantics() -> None:
    backend = _backend()
    doc = _document()
    backend.write(doc)
    restored = backend.read(doc.document_digest)
    assert restored.to_json() == doc.to_json()
    assert restored.document_digest == doc.document_digest
    assert restored.canonical_digest == doc.canonical_digest
    assert restored.scope == doc.scope
    assert backend.element_count(doc.document_digest) == 6  # 3 nodes + 2 rels + 1 version


def test_temporal_and_provenance_preserved() -> None:
    backend = _backend()
    doc = _document()
    backend.write(doc)
    versions = backend.elements_of_kind(doc.document_digest, "relationship_version")
    assert len(versions) == 1
    v = versions[0]
    assert v.effective_at == "2026-01-01"
    assert v.valid_to == "2026-12-31"
    assert v.payload["qualifiers"] == {"commitment": "firm"}
    nodes = backend.elements_of_kind(doc.document_digest, "node")
    supplier = next(n for n in nodes if n.element_id == persistence_element_id("node", "supplier-1"))
    assert supplier.provenance[0].source_ref == "erp:SUP-1"
    assert supplier.provenance[0].metadata == {"table": "suppliers"}


def test_write_is_idempotent() -> None:
    backend = _backend()
    doc = _document()
    backend.write(doc)
    before_count = backend.element_count(doc.document_digest)
    backend.write(doc)  # same document -> no-op
    assert backend.element_count(doc.document_digest) == before_count
    assert len(backend.list_document_digests()) == 1


def test_durable_after_transaction() -> None:
    conn = sqlite3.connect(":memory:")
    backend = RelationalGraphBackend(conn)
    doc = _document()
    backend.write(doc)
    # a second backend over the same connection sees the committed data
    backend2 = RelationalGraphBackend(conn)
    assert backend2.contains(doc.document_digest)
    assert backend2.read(doc.document_digest).to_json() == doc.to_json()


def test_digest_mismatch_rejected() -> None:
    backend = _backend()
    doc = _document()
    tampered = PersistedGraphDocument(
        scope=doc.scope,
        canonical_digest=doc.canonical_digest,
        elements=doc.elements,
        document_digest="0" * 64,
    )
    with pytest.raises(RelationalGraphBackendError, match="digest mismatch"):
        backend.write(tampered)
    assert not backend.contains(tampered.document_digest)


def test_read_missing_digest_rejected() -> None:
    backend = _backend()
    with pytest.raises(RelationalGraphBackendError, match="not found"):
        backend.read("deadbeef" * 8)


def test_list_and_contains() -> None:
    backend = _backend()
    d1 = _document()
    d2 = _document(scope="enterprise:other")
    backend.write(d1)
    backend.write(d2)
    digests = backend.list_document_digests()
    assert set(digests) == {d1.document_digest, d2.document_digest}
    assert backend.contains(d1.document_digest)
    assert not backend.contains("0" * 64)


def test_kind_index_query() -> None:
    backend = _backend()
    doc = _document()
    backend.write(doc)
    assert len(backend.elements_of_kind(doc.document_digest, "node")) == 3
    assert len(backend.elements_of_kind(doc.document_digest, "relationship")) == 2
    assert len(backend.elements_of_kind(doc.document_digest, "relationship_version")) == 1
    assert backend.elements_of_kind(doc.document_digest, "nonsense") == ()
