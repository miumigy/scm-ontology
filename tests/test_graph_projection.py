import pytest

from scm_ontology.graph_projection import (
    GraphNode,
    GraphProjection,
    GraphProjectionError,
    GraphRelationship,
    graph_projection_to_json,
)


def test_projection_is_deterministic_and_utf8_safe() -> None:
    projection = GraphProjection(
        nodes=(
            GraphNode("n2", "Location", (("name", "東京"),)),
            GraphNode("n1", "Supplier"),
        ),
        relationships=(
            GraphRelationship("r1", "SUPPLIES", "n1", "n2"),
        ),
        provenance_ids=("p2", "p1", "p2"),
    )

    payload = graph_projection_to_json(projection)
    assert payload == graph_projection_to_json(projection)
    assert "東京" in payload
    assert payload.index('"node_id":"n1"') < payload.index('"node_id":"n2"')
    assert projection.to_mapping()["provenance_ids"] == ["p1", "p2"]


def test_duplicate_node_id_is_rejected() -> None:
    with pytest.raises(GraphProjectionError, match="duplicate node_id"):
        GraphProjection(
            nodes=(GraphNode("n1", "Supplier"), GraphNode("n1", "Location")),
        )


def test_duplicate_relationship_id_is_rejected() -> None:
    with pytest.raises(GraphProjectionError, match="duplicate relationship_id"):
        GraphProjection(
            nodes=(GraphNode("n1", "Supplier"), GraphNode("n2", "Location")),
            relationships=(
                GraphRelationship("r1", "SUPPLIES", "n1", "n2"),
                GraphRelationship("r1", "SUPPLIES", "n1", "n2"),
            ),
        )


def test_relationship_endpoint_must_reference_projected_node() -> None:
    with pytest.raises(GraphProjectionError, match="endpoint"):
        GraphProjection(
            nodes=(GraphNode("n1", "Supplier"),),
            relationships=(GraphRelationship("r1", "SUPPLIES", "n1", "n2"),),
        )


def test_empty_identifiers_are_rejected() -> None:
    with pytest.raises(GraphProjectionError, match="node_id"):
        GraphNode(" ", "Supplier")

    with pytest.raises(GraphProjectionError, match="relationship"):
        GraphRelationship("r1", " ", "n1", "n2")
