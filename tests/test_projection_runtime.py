from scm_ontology.canonical_graph import CanonicalGraph, SemanticNode
from scm_ontology.projection_runtime import (
    PROTOCOL_VERSION,
    ProjectionDefinition,
    ProjectionError,
    materialize_projection,
    projection_to_json,
)


def graph() -> CanonicalGraph:
    return CanonicalGraph((SemanticNode("A", "Site", {"name": "東京"}),))


def definition() -> ProjectionDefinition:
    return ProjectionDefinition(
        "site-summary",
        "1",
        lambda source: {
            "site_count": len(source.nodes),
            "node_ids": [n.node_id for n in source.nodes],
            "site_names": [n.properties["name"] for n in source.nodes],
        },
    )


def test_projection_materializes_with_lineage() -> None:
    source = graph()
    before = source.to_json()
    result = materialize_projection(source, definition())

    assert result.contract_version == PROTOCOL_VERSION
    assert result.status == "materialized"
    assert result.value["site_count"] == 1
    assert len(result.source_digest) == 64
    assert result.lineage.source_digest == result.source_digest
    assert result.lineage.projection_id == "site-summary"
    assert source.to_json() == before


def test_projection_json_is_deterministic_and_utf8_safe() -> None:
    result = materialize_projection(graph(), definition())
    assert projection_to_json(result) == projection_to_json(result)
    assert "東京" in projection_to_json(result)


def test_projection_rejects_non_mapping_output() -> None:
    bad = ProjectionDefinition("bad", "1", lambda source: ["not-a-mapping"])
    try:
        materialize_projection(graph(), bad)
    except ProjectionError as exc:
        assert "mapping" in str(exc)
    else:
        raise AssertionError("expected ProjectionError")
