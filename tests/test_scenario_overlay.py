from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.relationship_identity import RelationshipInstance
from scm_ontology.relationship_version import RelationshipVersion
from scm_ontology.scenario_overlay import (
    ScenarioOperation,
    ScenarioOverlay,
    ScenarioOverlayError,
    execute_scenario_query,
    scenario_query_to_mapping,
)
from scm_ontology.temporal_semantic_query import TemporalSemanticQueryRequest


AT = "2026-08-16T00:00:00Z"


def _graph():
    return CanonicalGraph(
        nodes=(
            SemanticNode("a", "location"),
            SemanticNode("b", "location"),
            SemanticNode("c", "location"),
        ),
        relationships=(
            CanonicalRelationship(
                RelationshipInstance("r1", "a", "ships_to", "b"),
                (RelationshipVersion(AT, qualifiers={"lead_time_days": 2}),),
            ),
        ),
    )


def _r2():
    return CanonicalRelationship(
        RelationshipInstance("r2", "b", "ships_to", "c"),
        (RelationshipVersion(AT, qualifiers={"lead_time_days": 3}),),
    )


def test_scenario_add_enables_hypothetical_path_without_mutating_canonical_graph():
    graph = _graph()
    scenario = ScenarioOverlay("expedite-b-to-c", (ScenarioOperation("add", _r2()),))
    request = TemporalSemanticQueryRequest(AT, "a", "c", max_hops=3)

    before = graph.to_json()
    response = execute_scenario_query(graph, scenario, request)

    assert response.result.status == "resolved"
    assert response.result.paths[0].node_ids == ("a", "b", "c")
    assert response.base_graph_digest != response.result.graph_digest
    assert graph.to_json() == before
    assert len(graph.relationships) == 1


def test_scenario_digest_and_mapping_are_deterministic():
    scenario = ScenarioOverlay("expedite-b-to-c", (ScenarioOperation("add", _r2()),))
    request = TemporalSemanticQueryRequest(AT, "a", "c", max_hops=3)
    first = scenario_query_to_mapping(execute_scenario_query(_graph(), scenario, request))
    second = scenario_query_to_mapping(execute_scenario_query(_graph(), scenario, request))

    assert first == second
    assert first["contract_version"] == "1.0.0"
    assert first["scenario_id"] == "expedite-b-to-c"
    assert first["scenario_digest"]
    assert first["base_graph_digest"]


def test_scenario_remove_can_make_existing_path_temporally_absent():
    graph = _graph()
    scenario = ScenarioOverlay("remove-r1", (ScenarioOperation("remove", graph.relationships[0]),))
    request = TemporalSemanticQueryRequest(AT, "a", "b")

    response = execute_scenario_query(graph, scenario, request)

    assert response.result.status == "not_found"
    assert graph.relationships[0].instance.relationship_id == "r1"


def test_scenario_rejects_duplicate_relationship_operations():
    relationship = _r2()
    try:
        ScenarioOverlay(
            "invalid",
            (
                ScenarioOperation("add", relationship),
                ScenarioOperation("replace", relationship),
            ),
        )
    except ScenarioOverlayError:
        pass
    else:
        raise AssertionError("duplicate relationship operations must be rejected")
