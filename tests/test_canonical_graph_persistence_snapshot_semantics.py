import pytest

from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.canonical_graph_persistence import CanonicalGraphPersistenceError, InMemoryCanonicalGraphStore
from scm_ontology.relationship_identity import RelationshipInstance


def graph(name: str) -> CanonicalGraph:
    return CanonicalGraph(
        nodes=(SemanticNode("a", "Location", {"name": name}),),
        relationships=(CanonicalRelationship(RelationshipInstance("r1", "a", "connects_to", "a")),),
    )


def test_same_version_same_snapshot_is_idempotent():
    store = InMemoryCanonicalGraphStore()
    first = store.save("g1", graph("A"), graph_version="v1")
    second = store.save("g1", graph("A"), graph_version="v1")
    assert second == first
    assert store.load("g1", graph_version="v1").to_json() == graph("A").to_json()


def test_same_version_different_snapshot_is_rejected():
    store = InMemoryCanonicalGraphStore()
    store.save("g1", graph("A"), graph_version="v1")
    with pytest.raises(CanonicalGraphPersistenceError, match="version collision"):
        store.save("g1", graph("B"), graph_version="v1")


def test_new_version_preserves_old_snapshot_and_latest_load_is_deterministic():
    store = InMemoryCanonicalGraphStore()
    store.save("g1", graph("A"), graph_version="v1")
    store.save("g1", graph("B"), graph_version="v2")
    assert store.load("g1", graph_version="v1").to_json() == graph("A").to_json()
    assert store.load("g1", graph_version="v2").to_json() == graph("B").to_json()
    assert store.load("g1").to_json() == graph("B").to_json()


def test_missing_version_fails_closed():
    store = InMemoryCanonicalGraphStore()
    store.save("g1", graph("A"), graph_version="v1")
    with pytest.raises(CanonicalGraphPersistenceError, match="version not found"):
        store.load("g1", graph_version="v2")
