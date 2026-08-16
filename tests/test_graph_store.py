from dataclasses import replace

import pytest

from scm_ontology.canonical_graph import CanonicalGraph, SemanticNode
from scm_ontology.graph_persistence import (
    CanonicalGraphPersistencePlanner,
    PersistenceAuthorization,
)
from scm_ontology.graph_store import InMemoryGraphStore


def _plan(graph: CanonicalGraph):
    authorization = PersistenceAuthorization("decision-1", True, "test", "enterprise-a")
    return CanonicalGraphPersistencePlanner().plan(graph, authorization)


def test_in_memory_adapter_applies_authorized_plan_and_is_idempotent() -> None:
    graph = CanonicalGraph(nodes=(SemanticNode("p-1", "Product"),))
    plan = _plan(graph)
    store = InMemoryGraphStore()

    first = store.apply(graph, plan)
    replay = store.apply(graph, plan)

    assert first.outcome == "applied"
    assert first.replayed is False
    assert replay.replayed is True
    assert store.graph_count() == 1
    assert store.contains(plan.graph_digest)


def test_in_memory_adapter_rejects_digest_mismatch() -> None:
    graph = CanonicalGraph(nodes=(SemanticNode("p-1", "Product"),))
    plan = replace(_plan(graph), graph_digest="0" * 64)

    with pytest.raises(ValueError, match="graph digest"):
        InMemoryGraphStore().apply(graph, plan)


def test_in_memory_adapter_rejects_unplanned_intent() -> None:
    graph = CanonicalGraph(nodes=(SemanticNode("p-1", "Product"),))
    authorization = PersistenceAuthorization("decision-2", False, "test", "enterprise-a")
    plan = CanonicalGraphPersistencePlanner().plan(graph, authorization)
    store = InMemoryGraphStore()

    with pytest.raises(ValueError, match="only an authorized planned"):
        store.apply(graph, plan)

    assert store.graph_count() == 0
