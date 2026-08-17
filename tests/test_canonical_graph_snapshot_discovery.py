import pytest

from scm_ontology.canonical_graph import CanonicalGraph
from scm_ontology.canonical_graph_persistence import (
    CanonicalGraphPersistenceError,
    InMemoryCanonicalGraphStore,
)


def graph() -> CanonicalGraph:
    return CanonicalGraph(nodes=(), relationships=())


def test_snapshot_discovery_is_deterministic_and_metadata_preserving():
    store = InMemoryCanonicalGraphStore()
    store.save("g2", graph(), graph_version="2", schema_version="s1")
    store.save("g1", graph(), graph_version="10", schema_version="s2")
    store.save("g1", graph(), graph_version="2", schema_version="s1")

    assert store.list_graph_ids() == ("g1", "g2")
    assert store.list_versions("g1") == ("10", "2")
    snapshots = store.list_snapshots("g1")
    assert tuple(s.graph_version for s in snapshots) == ("10", "2")
    assert snapshots[0].schema_version == "s2"


def test_latest_version_is_explicit_and_deterministic():
    store = InMemoryCanonicalGraphStore()
    store.save("g1", graph(), graph_version="1")
    store.save("g1", graph(), graph_version="3")
    assert store.latest_version("g1") == "3"


def test_missing_graph_discovery_fails_closed():
    store = InMemoryCanonicalGraphStore()
    with pytest.raises(CanonicalGraphPersistenceError, match="graph_id not found"):
        store.list_versions("missing")
    with pytest.raises(CanonicalGraphPersistenceError, match="graph_id not found"):
        store.latest_version("missing")
