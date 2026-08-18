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
from scm_ontology.neo4j_graph_backend import Neo4jGraphBackend, Neo4jGraphBackendError
from scm_ontology.relational_graph_backend import RelationalGraphBackend, PersistentGraphBackendError


def _graph() -> CanonicalGraph:
    return CanonicalGraph(
        nodes=(
            SemanticNode("supplier-1", "Supplier", {"name": "Acme"}),
            SemanticNode("factory-1", "Factory"),
        ),
        relationships=(
            CanonicalRelationship(
                RelationshipInstance("rel-1", "supplier-1", "supplies", "factory-1"),
                (RelationshipVersion("2026-01-01", "2026-12-31", {"commitment": "firm"}),),
            ),
        ),
    )


def _document(scope="enterprise:acme") -> PersistedGraphDocument:
    provenance = {
        persistence_element_id("node", "supplier-1"): (
            EvidenceRef("erp:SUP-1", observed_at="2026-08-19T09:00:00Z", metadata={"table": "suppliers"}),
        ),
        persistence_element_id("relationship", "rel-1"): (EvidenceRef("tms:assets-1"),),
    }
    return persistent_graph_document(_graph(), scope=scope, provenance=provenance)


class _Row(tuple):
    pass


class FakeNeo4j:
    """Deterministic in-memory 'Neo4j' that structurally interprets the
    statements emitted by ``Neo4jGraphBackend``.

    Documents are keyed by document_digest; elements carry position/kind/payload
    and temporal fields; provenance is stored per element and replayed as
    relationships. This is a test transport double, not a Cypher engine.
    """

    def __init__(self):
        self.documents: dict[str, dict] = {}
        self.elements: dict[str, dict[str, dict]] = {}
        self.provenance: dict[str, dict[str, list[tuple]]] = {}

    def execute(self, statement, params):
        if "CanonicalDocument" in statement:
            self.documents[params["digest"]] = {
                "scope": params["scope"],
                "canonical_digest": params["canonical_digest"],
            }
        elif "CanonicalProvenance" in statement:
            bucket = self.provenance.setdefault(params["digest"], {})
            bucket.setdefault(params["element_id"], []).append(
                (params["source_ref"], params.get("observed_at"), params.get("metadata"))
            )
        else:  # CanonicalElement
            d = self.elements.setdefault(params["digest"], {})
            d[params["element_id"]] = {
                "position": params["position"],
                "kind": params["kind"],
                "payload": params["payload"],
                "effective_at": params.get("effective_at"),
                "valid_to": params.get("valid_to"),
                "observed_at": params.get("observed_at"),
            }

    def query(self, statement, params):
        digest = params.get("digest")
        # provenance: (e)-[:HAS_PROVENANCE]->(p) and RETURN e.element_id, hp.source_ref...
        if "HAS_PROVENANCE" in statement and "RETURN e.element_id, hp.source_ref" in statement:
            if digest not in self.provenance:
                return ()
            kind = params.get("kind")
            rows = []
            for element_id in sorted(self.provenance[digest]):
                if kind is not None and self.elements.get(digest, {}).get(element_id, {}).get("kind") != kind:
                    continue
                for source_ref, observed_at, metadata in sorted(self.provenance[digest][element_id]):
                    rows.append((element_id, source_ref, observed_at, metadata))
            return tuple(rows)

        # element rows
        if "RETURN e.element_id, e.kind" in statement:
            els = self.elements.get(digest, {})
            if "kind" in params:
                els = {k: v for k, v in els.items() if v["kind"] == params["kind"]}
            ordered = sorted(els.items(), key=lambda kv: kv[1]["position"])
            return tuple(
                (element_id, props["kind"], props["payload"], props["effective_at"],
                 props["valid_to"], props["observed_at"])
                for element_id, props in ordered
            )

        # element count aggregate
        if "count(" in statement and "CanonicalElement" in statement:
            els = self.elements.get(digest, {})
            if "kind" in params:
                els = {k: v for k, v in els.items() if v["kind"] == params["kind"]}
            return ((len(els),),)

        # document read (scope, canonical_digest)
        if "RETURN d.scope" in statement:
            if digest not in self.documents:
                return ()
            d = self.documents[digest]
            return ((d["scope"], d["canonical_digest"]),)

        # contains (RETURN d.document_digest with digest filter)
        if "RETURN d.document_digest" in statement and "ORDER BY" not in statement:
            return ((digest,) if digest in self.documents else ())

        # list (no digest filter, ORDER BY)
        if "RETURN d.document_digest" in statement and "ORDER BY" in statement:
            return tuple((d,) for d in sorted(self.documents))

        return ()


def _neo4j_backend() -> tuple[Neo4jGraphBackend, FakeNeo4j]:
    fake = FakeNeo4j()
    return Neo4jGraphBackend(fake.execute, fake.query), fake


def test_write_emits_mapping_statements_with_payload() -> None:
    captures = []

    def execute(stmt, params):
        captures.append((stmt, params))

    def query(stmt, params):
        if "RETURN d.scope" in stmt:
            return (("enterprise:acme", "canonical"),)
        return ()

    backend = Neo4jGraphBackend(execute, query)
    doc = _document()
    # contains -> no rows -> proceeds to write
    backend.write(doc)
    statements = [s for s, _ in captures]
    assert any("CanonicalDocument" in s for s in statements)
    assert any("CanonicalElement" in s for s in statements)
    assert any("CanonicalProvenance" in s for s in statements)
    # element order preserved (relationship version after its relationship)
    doc_stmt = next(
        (params for s, params in captures if "CanonicalElement" in s and "CanonicalProvenance" not in s
         and params["element_id"] == "relationship:rel-1"),
        None,
    )
    assert doc_stmt is not None
    assert "relationship_id" in doc_stmt["payload"]


def test_write_rejects_digest_mismatch_before_any_statement() -> None:
    calls = []

    def execute(stmt, params):
        calls.append(stmt)

    backend = Neo4jGraphBackend(execute, lambda s, p: ())
    doc = _document()
    tampered = PersistedGraphDocument(
        scope=doc.scope, canonical_digest=doc.canonical_digest, elements=doc.elements, document_digest="0" * 64
    )
    with pytest.raises(Neo4jGraphBackendError, match="digest mismatch"):
        backend.write(tampered)
    assert calls == []


def test_write_rejects_empty_digest() -> None:
    calls = []
    fake = FakeNeo4j()
    backend = Neo4jGraphBackend(fake.execute, fake.query)
    doc = _document()
    bad = PersistedGraphDocument(scope=doc.scope, canonical_digest=doc.canonical_digest, elements=doc.elements)
    with pytest.raises(Neo4jGraphBackendError, match="document_digest"):
        backend.write(bad)


def test_write_read_roundtrip_preserves_semantics() -> None:
    backend, fake = _neo4j_backend()
    doc = _document()
    backend.write(doc)
    restored = backend.read(doc.document_digest)
    assert restored.to_json() == doc.to_json()
    assert backend.element_count(doc.document_digest) == 4  # 2 nodes + 1 rel + 1 version
    assert backend.contains(doc.document_digest)
    versions = backend.elements_of_kind(doc.document_digest, "relationship_version")
    assert len(versions) == 1
    assert versions[0].effective_at == "2026-01-01"
    assert versions[0].payload["qualifiers"] == {"commitment": "firm"}


def test_write_is_idempotent() -> None:
    backend, _ = _neo4j_backend()
    doc = _document()
    backend.write(doc)
    before = backend.element_count(doc.document_digest)
    backend.write(doc)
    assert backend.element_count(doc.document_digest) == before
    assert len(backend.list_document_digests()) == 1


def test_read_missing_digest_rejected() -> None:
    backend, _ = _neo4j_backend()
    with pytest.raises(PersistentGraphBackendError, match="not found"):
        backend.read("0" * 64)


def test_equivalence_with_relational_backend() -> None:
    """P8-F premise: the two reference backends must produce identical
    canonical/query semantics for the same P8-A document."""
    import json as _json
    import sqlite3

    doc = _document()
    rel_backend = RelationalGraphBackend(sqlite3.connect(":memory:"))
    neo_backend, fake = _neo4j_backend()
    rel_backend.write(doc)
    neo_backend.write(doc)
    assert neo_backend.read(doc.document_digest).to_json() == rel_backend.read(doc.document_digest).to_json()
    assert neo_backend.element_count(doc.document_digest) == rel_backend.element_count(doc.document_digest)
    assert set(neo_backend.list_document_digests()) == set(rel_backend.list_document_digests())


def _sample() -> PersistedGraphDocument:
    provenance = {
        persistence_element_id("node", "supplier-1"): (
            EvidenceRef("erp:SUP-1", observed_at="2026-08-19T09:00:00Z", metadata={"table": "suppliers"}),
        ),
        persistence_element_id("relationship", "rel-1"): (EvidenceRef("tms:assets-1"),),
    }
    return persistent_graph_document(_graph(), scope="enterprise:acme", provenance=provenance)
