import sqlite3

import pytest

from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.evidence_provenance import EvidenceRef
from scm_ontology.persistent_graph_contract import (
    persistence_element_id,
    persistent_graph_document,
)
from scm_ontology.relationship_identity import RelationshipInstance
from scm_ontology.relationship_version import RelationshipVersion
from scm_ontology.relational_graph_backend import RelationalGraphBackend
from scm_ontology.persistent_query_surface import (
    BackedQuerySurface,
    DocumentQuerySurface,
    INDEX_EXPECTATIONS,
    PersistentQuerySurfaceError,
)

# Import the P8-C neo4j backend and its test double for cross-backend equivalence.
from tests.test_neo4j_graph_backend import FakeNeo4j
from scm_ontology.neo4j_graph_backend import Neo4jGraphBackend


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


def _document(scope="enterprise:acme"):
    provenance = {
        persistence_element_id("node", "supplier-1"): (
            EvidenceRef("erp:SUP-1", observed_at="2026-08-19T09:00:00Z"),
        )
    }
    return persistent_graph_document(_graph(), scope=scope, provenance=provenance)


def _doc_surface(doc=None):
    return DocumentQuerySurface(doc or _document())


def test_index_expectations_explicit() -> None:
    assert set(INDEX_EXPECTATIONS) == {"element_id", "kind", "effective_at", "source_ref"}


def test_document_surface_element_by_id() -> None:
    surf = _doc_surface()
    el = surf.element_by_id(persistence_element_id("node", "supplier-1"))
    assert el is not None and el.kind == "node"
    assert surf.element_by_id("nope") is None


def test_document_surface_kind_and_count() -> None:
    surf = _doc_surface()
    assert surf.element_count() == 4  # 2 nodes + 1 relationship + 1 version
    assert len(surf.elements_of_kind("node")) == 2
    assert len(surf.elements_of_kind("relationship")) == 1
    assert len(surf.elements_of_kind("relationship_version")) == 1


def test_document_surface_effective_at_and_provenance() -> None:
    surf = _doc_surface()
    eff = surf.elements_effective_at("2026-01-01")
    assert len(eff) == 1 and eff[0].kind == "relationship_version"
    prov = surf.elements_with_provenance("erp:SUP-1")
    assert len(prov) == 1 and prov[0].element_id == persistence_element_id("node", "supplier-1")


def test_relational_backed_surface_uses_indexed_queries() -> None:
    doc = _document()
    rel = RelationalGraphBackend(sqlite3.connect(":memory:"))
    rel.write(doc)
    surf = BackedQuerySurface(rel, doc.document_digest)
    # element_by_id / elements_of_kind exercise the backend's own index methods
    node = surf.element_by_id(persistence_element_id("node", "supplier-1"))
    assert node is not None and node.kind == "node"
    assert [el.element_id for el in surf.elements_of_kind("relationship_version")] == [
        persistence_element_id("relationship_version", "rel-1#v:2026-01-01")
    ]
    assert len(surf.elements_effective_at("2026-01-01")) == 1
    assert len(surf.elements_with_provenance("erp:SUP-1")) == 1
    assert surf.element_count() == 4


def test_document_and_relational_backed_surfaces_equivalent() -> None:
    doc = _document()
    rel = RelationalGraphBackend(sqlite3.connect(":memory:"))
    rel.write(doc)
    doc_surf = DocumentQuerySurface(doc)
    rel_surf = BackedQuerySurface(rel, doc.document_digest)
    for kind in ("node", "relationship", "relationship_version"):
        assert {e.element_id for e in doc_surf.elements_of_kind(kind)} == \
               {e.element_id for e in rel_surf.elements_of_kind(kind)}
    assert doc_surf.element_count() == rel_surf.element_count()


def test_cross_backend_semantic_equivalence() -> None:
    """Relational (P8-B) and Neo4j (P8-C) backends give identical query answers
    because they reconstruct the same P8-A document (P8-E index boundary)."""
    import json as _json

    doc = _document()
    rel = RelationalGraphBackend(sqlite3.connect(":memory:"))
    rel.write(doc)
    fake = FakeNeo4j()
    neo = Neo4jGraphBackend(fake.execute, fake.query)
    neo.write(doc)

    rel_surf = DocumentQuerySurface(rel.read(doc.document_digest))
    neo_surf = DocumentQuerySurface(neo.read(doc.document_digest))
    assert rel_surf.element_count() == neo_surf.element_count() == 4
    for kind in ("node", "relationship", "relationship_version"):
        assert {e.element_id for e in rel_surf.elements_of_kind(kind)} == \
               {e.element_id for e in neo_surf.elements_of_kind(kind)}
    assert {e.element_id for e in rel_surf.elements_with_provenance("erp:SUP-1")} == \
           {e.element_id for e in neo_surf.elements_with_provenance("erp:SUP-1")}
