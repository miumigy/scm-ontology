from dataclasses import replace

import pytest

from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.graph_persistence import CanonicalGraphPersistencePlanner, PersistenceAuthorization
from scm_ontology.neo4j_adapter import Neo4jGraphStoreAdapter
from scm_ontology.relationship_identity import RelationshipInstance


def _graph() -> CanonicalGraph:
    return CanonicalGraph(
        nodes=(
            SemanticNode("supplier-1", "Supplier", {"name": "Acme"}),
            SemanticNode("factory-1", "Factory"),
        ),
        relationships=(
            CanonicalRelationship(
                RelationshipInstance("rel-1", "supplier-1", "supplies", "factory-1")
            ),
        ),
    )


def _plan(graph: CanonicalGraph, authorized: bool = True):
    return CanonicalGraphPersistencePlanner().plan(
        graph, PersistenceAuthorization("d-1", authorized, "test", "scope-a")
    )


def test_neo4j_adapter_injects_governed_transport_payload() -> None:
    calls = []

    def execute(query, params):
        calls.append((query, params))

    graph = _graph()
    plan = _plan(graph)
    result = Neo4jGraphStoreAdapter(execute).apply(graph, plan)

    assert result.outcome == "applied"
    assert result.graph_digest == plan.graph_digest
    assert len(calls) == 1
    query, params = calls[0]
    assert "CanonicalPersistencePlan" in query
    assert "CANONICAL_RELATIONSHIP" in query
    assert params["plan_id"] == plan.plan_id
    assert params["graph_digest"] == plan.graph_digest
    assert params["nodes"][0]["id"] == "supplier-1"
    assert params["relationships"][0]["predicate"] == "supplies"


def test_neo4j_adapter_rejects_digest_mismatch_before_transport() -> None:
    calls = []
    graph = _graph()
    plan = replace(_plan(graph), graph_digest="0" * 64)

    with pytest.raises(ValueError, match="graph digest"):
        Neo4jGraphStoreAdapter(lambda q, p: calls.append((q, p))).apply(graph, plan)

    assert calls == []


def test_neo4j_adapter_rejects_unplanned_intent() -> None:
    calls = []
    graph = _graph()
    plan = _plan(graph, authorized=False)

    with pytest.raises(ValueError, match="planned"):
        Neo4jGraphStoreAdapter(lambda q, p: calls.append((q, p))).apply(graph, plan)

    assert calls == []
