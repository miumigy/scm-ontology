import pytest

from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.canonical_graph_persistence import (
    CanonicalGraphPersistenceError,
    InMemoryCanonicalGraphStore,
    graph_identity,
)
from scm_ontology.relationship_identity import RelationshipInstance


def sample_graph() -> CanonicalGraph:
    return CanonicalGraph(
        nodes=(
            SemanticNode("b", "Location", {"name": "B"}),
            SemanticNode("a", "Location", {"name": "A"}),
        ),
        relationships=(
            CanonicalRelationship(
                RelationshipInstance("r1", "a", "connects_to", "b")
            ),
        ),
    )


def test_save_load_round_trip_preserves_canonical_identity():
    store = InMemoryCanonicalGraphStore()
    graph = sample_graph()

    stored = store.save("g1", graph)
    restored = store.load("g1")

    assert stored.graph_id == "g1"
    assert stored.document == graph.to_json()
    assert restored.to_json() == graph.to_json()
    assert graph_identity(restored) == graph_identity(graph)


def test_persistence_is_deterministic_and_transport_neutral():
    graph = sample_graph()
    first = InMemoryCanonicalGraphStore().save("g1", graph)
    second = InMemoryCanonicalGraphStore().save("g1", graph)

    assert first.document == second.document
    assert graph_identity(graph) == graph_identity(graph)


def test_missing_graph_fails_closed():
    with pytest.raises(CanonicalGraphPersistenceError, match="not found"):
        InMemoryCanonicalGraphStore().load("missing")


def test_blank_graph_id_is_rejected():
    store = InMemoryCanonicalGraphStore()
    with pytest.raises(CanonicalGraphPersistenceError, match="graph_id must be non-empty"):
        store.save(" ", sample_graph())


def test_store_does_not_mutate_graph():
    graph = sample_graph()
    before = graph.to_json()
    store = InMemoryCanonicalGraphStore()

    store.save("g1", graph)

    assert graph.to_json() == before
