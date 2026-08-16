from dataclasses import replace

from scm_ontology.canonical_graph import CanonicalGraph, SemanticNode
from scm_ontology.projection_lifecycle import (
    assess_projection_freshness,
    invalidate_projection,
    projection_lifecycle_to_json,
    rebuild_projection,
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


def test_projection_is_current_when_dependencies_match() -> None:
    source = graph()
    result = materialize_projection(source, definition())

    lifecycle = assess_projection_freshness(source, definition(), result)

    assert lifecycle.state == "current"
    assert lifecycle.reason == "dependencies_match"


def test_source_change_marks_projection_stale_without_mutation() -> None:
    source = graph()
    result = materialize_projection(source, definition())
    changed = graph("大阪")
    before = changed.to_json()

    lifecycle = assess_projection_freshness(changed, definition(), result)

    assert lifecycle.state == "stale"
    assert lifecycle.reason == "source_digest_changed"
    assert changed.to_json() == before


def test_projection_definition_change_requires_rebuild() -> None:
    result = materialize_projection(graph(), definition("1"))

    lifecycle = assess_projection_freshness(graph(), definition("2"), result)

    assert lifecycle.state == "rebuild_required"
    assert lifecycle.reason == "projection_version_mismatch"


def test_explicit_invalidation_is_observable_and_json_safe() -> None:
    result = materialize_projection(graph(), definition())

    lifecycle = invalidate_projection(result, "upstream_dependency_invalidated")
    payload = projection_lifecycle_to_json(lifecycle)

    assert lifecycle.state == "invalid"
    assert "upstream_dependency_invalidated" in payload
    assert "東京" not in payload


def test_rebuild_recomputes_from_current_graph() -> None:
    original = materialize_projection(graph(), definition())
    rebuilt = rebuild_projection(graph("大阪"), definition())

    assert original.source_digest != rebuilt.source_digest
    assert rebuilt.value["site_names"] == ["大阪"]


def test_non_materialized_result_is_invalid() -> None:
    result = materialize_projection(graph(), definition())
    invalid = replace(result, status="failed")

    lifecycle = assess_projection_freshness(graph(), definition(), invalid)

    assert lifecycle.state == "invalid"
    assert lifecycle.reason == "result_not_materialized"
