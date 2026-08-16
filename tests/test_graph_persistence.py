from hashlib import sha256

from scm_ontology.canonical_graph import CanonicalGraph, SemanticNode
from scm_ontology.graph_persistence import (
    CanonicalGraphPersistencePlanner,
    PersistenceAuthorization,
)


def test_authorized_plan_is_deterministic_and_non_mutating() -> None:
    graph = CanonicalGraph(nodes=(SemanticNode("p-1", "Product", {"name": "Widget"}),))
    auth = PersistenceAuthorization("decision-1", True, "planner-test", "enterprise-a")
    planner = CanonicalGraphPersistencePlanner()

    first = planner.plan(graph, auth)
    second = planner.plan(graph, auth)

    assert first == second
    assert first.outcome == "planned"
    assert first.node_ids == ("p-1",)
    assert first.relationship_ids == ()
    assert first.graph_digest == sha256(graph.to_json().encode()).hexdigest()
    assert graph.nodes[0].properties["name"] == "Widget"


def test_unauthorized_plan_is_rejected_without_graph_mutation() -> None:
    graph = CanonicalGraph(nodes=(SemanticNode("p-1", "Product"),))
    auth = PersistenceAuthorization(
        "decision-2", False, "planner-test", "enterprise-a", "scope not authorized"
    )

    plan = CanonicalGraphPersistencePlanner().plan(graph, auth)

    assert plan.outcome == "rejected"
    assert plan.reason == "scope not authorized"
    assert plan.graph_digest == sha256(graph.to_json().encode()).hexdigest()
    assert graph.nodes[0].node_id == "p-1"
