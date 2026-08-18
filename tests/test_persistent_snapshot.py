import sqlite3

import pytest

from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.evidence_provenance import EvidenceRef
from scm_ontology.persistent_graph_contract import persistence_element_id, persistent_graph_document
from scm_ontology.persistent_snapshot import SnapshotError, VersionedGraphBackend
from scm_ontology.relationship_identity import RelationshipInstance
from scm_ontology.relationship_version import RelationshipVersion
from scm_ontology.relational_graph_backend import RelationalGraphBackend


def _graph(with_version=True) -> CanonicalGraph:
    rels = [
        CanonicalRelationship(RelationshipInstance("rel-1", "supplier-1", "supplies", "factory-1"))
    ]
    if with_version:
        rels = [
            CanonicalRelationship(
                RelationshipInstance("rel-1", "supplier-1", "supplies", "factory-1"),
                (RelationshipVersion("2026-01-01", "2026-12-31", {"commitment": "firm"}),),
            )
        ]
    return CanonicalGraph(
        nodes=(
            SemanticNode("supplier-1", "Supplier", {"name": "Acme"}),
            SemanticNode("factory-1", "Factory"),
        ),
        relationships=tuple(rels),
    )


def _doc(graph=None, scope="enterprise:acme"):
    provenance = {
        persistence_element_id("node", "supplier-1"): (
            EvidenceRef("erp:SUP-1", observed_at="2026-08-19T09:00:00Z"),
        )
    }
    return persistent_graph_document(graph or _graph(), scope=scope, provenance=provenance)


def _versioned() -> VersionedGraphBackend:
    return VersionedGraphBackend(RelationalGraphBackend(sqlite3.connect(":memory:")))


def test_capture_and_replay_roundtrip() -> None:
    v = _versioned()
    doc = _doc()
    snap = v.capture(doc, graph_id="acme-net", version="v1", created_at="2026-08-19T00:00:00Z")
    assert snap.document_digest == doc.document_digest
    replayed = v.replay("acme-net", "v1")
    assert replayed.to_json() == doc.to_json()


def test_snapshot_is_deterministic() -> None:
    v1 = _versioned()
    v2 = _versioned()
    doc = _doc()
    s1 = v1.capture(doc, graph_id="acme-net", version="v1", created_at="2026-08-19T00:00:00Z")
    s2 = v2.capture(doc, graph_id="acme-net", version="v1", created_at="2026-08-19T00:00:00Z")
    assert s1.snapshot_id == s2.snapshot_id


def test_version_sequence_and_replay_historical() -> None:
    v = _versioned()
    v.capture(_doc(_graph(with_version=False)), graph_id="acme-net", version="v1")
    v.capture(_doc(), graph_id="acme-net", version="v2")
    assert v.list_versions("acme-net") == ("v1", "v2")
    assert v.latest_version("acme-net") == "v2"
    # replay reproduces historical state exactly (v1 has no temporal version)
    r1 = v.replay("acme-net", "v1")
    kinds = {el.kind for el in r1.elements}
    assert "relationship_version" not in kinds


def test_replay_graph_reconstructs_canonical_graph() -> None:
    v = _versioned()
    doc = _doc()
    v.capture(doc, graph_id="acme-net", version="v1")
    g = v.replay_graph("acme-net", "v1")
    assert {n.node_id for n in g.nodes} == {"supplier-1", "factory-1"}
    assert len(g.relationships) == 1
    assert g.relationships[0].versions[0].valid_from == "2026-01-01"


def test_version_collision_rejected() -> None:
    v = _versioned()
    v.capture(_doc(_graph(with_version=False)), graph_id="acme-net", version="v1")
    with pytest.raises(SnapshotError, match="collision"):
        v.capture(_doc(), graph_id="acme-net", version="v1")


def test_replay_missing_version_rejected() -> None:
    v = _versioned()
    v.capture(_doc(), graph_id="acme-net", version="v1")
    with pytest.raises(SnapshotError, match="not found"):
        v.replay("acme-net", "v9")
    with pytest.raises(SnapshotError, match="no versions"):
        v.replay("other-net", "v1")


def test_fail_closed_empty_identifiers() -> None:
    v = _versioned()
    doc = _doc()
    with pytest.raises(SnapshotError, match="graph_id"):
        v.capture(doc, graph_id="  ", version="v1")
    with pytest.raises(SnapshotError, match="version"):
        v.capture(doc, graph_id="acme-net", version="")


def test_replay_is_idempotent_across_backends() -> None:
    """Replay through the relational (P8-B) backend reproduces the document."""
    v = _versioned()
    doc = _doc()
    v.capture(doc, graph_id="acme-net", version="v1")
    for _ in range(3):
        assert v.replay("acme-net", "v1").to_json() == doc.to_json()
