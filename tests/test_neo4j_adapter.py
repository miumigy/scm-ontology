from scm_ontology.canonical_graph import CanonicalGraph, SemanticNode
from scm_ontology.graph_persistence import CanonicalGraphPersistencePlanner, PersistenceAuthorization
from scm_ontology.neo4j_adapter import Neo4jGraphStoreAdapter


def test_neo4j_adapter_injects_only_transport_payload() -> None:
    calls = []

    def execute(query, params):
        calls.append((query, params))

    graph = CanonicalGraph(nodes=(SemanticNode("p-1", "Product", {"name": "Widget"}),))
    plan = CanonicalGraphPersistencePlanner().plan(
        graph, PersistenceAuthorization("d-1", True, "test", "scope-a")
    )

    result = Neo4jGraphStoreAdapter(execute).apply(graph, plan)

    assert result.outcome == "applied"
    assert result.graph_digest == plan.graph_digest
    assert len(calls) == 1
    assert calls[0][1]["nodes"][0]["id"] == "p-1"


def test_neo4j_adapter_rejects_unplanned_intent() -> None:
    calls = []
    graph = CanonicalGraph(nodes=(SemanticNode("p-1", "Product"),))
    plan = CanonicalGraphPersistencePlanner().plan(
        graph, PersistenceAuthorization("d-2", False, "test", "scope-a")
    )

    try:
        Neo4jGraphStoreAdapter(lambda q, p: calls.append((q, p))).apply(graph, plan)
    except ValueError as exc:
        assert "planned" in str(exc)
    else:
        raise AssertionError("unplanned persistence intent must be rejected")

    assert calls == []
