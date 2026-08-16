from dataclasses import replace

from scm_ontology.canonical_graph import CanonicalGraph, SemanticNode
from scm_ontology.projection_query import (
    ProjectionQueryRequest,
    execute_projection_query,
    query_response_to_mapping,
)
from scm_ontology.projection_runtime import ProjectionDefinition, materialize_projection


def graph(name: str = "東京") -> CanonicalGraph:
    return CanonicalGraph((SemanticNode("A", "Site", {"name": name}),))


def definition(version: str = "1") -> ProjectionDefinition:
    return ProjectionDefinition(
        "site-summary",
        version,
        lambda source: {"site_names": [n.properties["name"] for n in source.nodes]},
    )


def request(version: str = "1") -> ProjectionQueryRequest:
    return ProjectionQueryRequest("site-summary", version)


def test_query_resolves_current_projection_with_lifecycle() -> None:
    source = graph()
    result = materialize_projection(source, definition())

    response = execute_projection_query(
        request(), graph=source, definition=definition(), result=result
    )

    assert response.status == "resolved"
    assert response.projection["value"]["site_names"] == ["東京"]
    assert response.lifecycle["state"] == "current"


def test_query_fails_closed_for_stale_projection() -> None:
    result = materialize_projection(graph(), definition())

    response = execute_projection_query(
        request(), graph=graph("大阪"), definition=definition(), result=result
    )

    assert response.status == "stale"
    assert response.projection is None
    assert response.lifecycle["reason"] == "source_digest_changed"


def test_query_fails_closed_for_rebuild_required_projection() -> None:
    result = materialize_projection(graph(), definition("1"))

    response = execute_projection_query(
        request("2"), graph=graph(), definition=definition("2"), result=result
    )

    assert response.status == "rebuild_required"
    assert response.projection is None
    assert response.lifecycle["reason"] == "projection_version_mismatch"


def test_query_fails_closed_for_invalid_materialization() -> None:
    result = materialize_projection(graph(), definition())
    invalid = replace(result, status="failed")

    response = execute_projection_query(
        request(), graph=graph(), definition=definition(), result=invalid
    )

    assert response.status == "invalid"
    assert response.projection is None
    assert response.error == "result_not_materialized"


def test_query_rejects_contract_mismatch() -> None:
    result = materialize_projection(graph(), definition())
    response = execute_projection_query(
        ProjectionQueryRequest("site-summary", "1", contract_version="0.9.0"),
        graph=graph(),
        definition=definition(),
        result=result,
    )

    assert response.status == "contract_version_mismatch"
    assert response.projection is None


def test_query_response_mapping_is_json_safe_and_deterministic() -> None:
    result = materialize_projection(graph(), definition())
    response = execute_projection_query(
        request(), graph=graph(), definition=definition(), result=result
    )

    mapping = query_response_to_mapping(response)

    assert mapping == query_response_to_mapping(response)
    assert mapping["contract_version"] == "1.0.0"
    assert mapping["projection"]["value"]["site_names"] == ["東京"]
