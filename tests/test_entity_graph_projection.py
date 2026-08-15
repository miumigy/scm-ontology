from scm_ontology.entity_graph_projection import (
    CanonicalEntityGraphNode,
    project_canonical_entities,
)


def test_canonical_entity_projection_preserves_identity_and_properties() -> None:
    nodes = project_canonical_entities(
        [
            {
                "type": "Product",
                "id": "product:1",
                "properties": {"name": "Widget", "uom": "EA"},
            }
        ]
    )
    assert nodes == (
        CanonicalEntityGraphNode(
            "Product",
            "product:1",
            (("name", "Widget"), ("uom", "EA")),
        ),
    )
