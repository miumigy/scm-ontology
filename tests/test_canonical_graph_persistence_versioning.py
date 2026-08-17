import pytest

from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.canonical_graph_persistence import (
    CanonicalGraphPersistenceError,
    InMemoryCanonicalGraphStore,
)
from scm_ontology.relationship_identity import RelationshipInstance


def sample_graph() -> CanonicalGraph:
    return CanonicalGraph(
        nodes=(
            SemanticNode("b", "Location", {"name": "B"}),
            SemanticNode("a", "Location", {"name": "A"}),
        ),
        relationships=(CanonicalRelationship(RelationshipInstance("r1", "a", "connects_to", "b")),),
    )


def test_versioned_snapshot_contains_deterministic_integrity_metadata():
    stored = InMemoryCanonicalGraphStore().save(
        "g1", sample_graph(), graph_version="2026-08-17", schema_version="1"
    )
    assert stored.graph_id == "g1"
    assert stored.graph_version == "2026-08-17"
    assert stored.schema_version == "1"
    assert stored.canonical_identity
    assert stored.payload_integrity == stored.canonical_identity


def test_versioned_save_is_deterministic():
    graph = sample_graph()
    first = InMemoryCanonicalGraphStore().save("g1", graph, graph_version="v1", schema_version="s1")
    second = InMemoryCanonicalGraphStore().save("g1", graph, graph_version="v1", schema_version="s1")
    assert first == second


def test_blank_versions_are_rejected():
    store = InMemoryCanonicalGraphStore()
    with pytest.raises(CanonicalGraphPersistenceError, match="graph_version must be non-empty"):
        store.save("g1", sample_graph(), graph_version=" ")
    with pytest.raises(CanonicalGraphPersistenceError, match="schema_version must be non-empty"):
        store.save("g1", sample_graph(), schema_version=" ")
