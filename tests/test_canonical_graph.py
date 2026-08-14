import json

import pytest

from scm_ontology.canonical_graph import (
    CanonicalGraph,
    CanonicalGraphError,
    CanonicalRelationship,
    SemanticNode,
)
from scm_ontology.relationship_identity import RelationshipInstance
from scm_ontology.relationship_version import RelationshipVersion


def test_canonical_graph_preserves_identity_and_versions():
    graph = CanonicalGraph(
        nodes=(
            SemanticNode("order-1", "CustomerOrder"),
            SemanticNode("supplier-1", "Supplier"),
        ),
        relationships=(
            CanonicalRelationship(
                RelationshipInstance("r1", "order-1", "supplied_by", "supplier-1"),
                versions=(
                    RelationshipVersion(
                        "2026-01-01",
                        "2026-06-30",
                        {"priority": 1},
                    ),
                    RelationshipVersion("2026-07-01", None, {"priority": 2}),
                ),
            ),
        ),
    )

    document = graph.to_mapping()

    assert document["nodes"][0]["id"] == "order-1"
    assert document["relationships"][0]["id"] == "r1"
    assert document["relationships"][0]["from"] == "order-1"
    assert document["relationships"][0]["versions"][1]["valid_to"] is None
    assert document["relationships"][0]["versions"][0]["qualifiers"] == {"priority": 1}


def test_json_serialization_is_deterministic_and_unicode_safe():
    graph = CanonicalGraph(nodes=(SemanticNode("n1", "商品", {"name": "部品"}),))

    serialized = graph.to_json()

    assert json.loads(serialized)["nodes"][0]["properties"]["name"] == "部品"
    assert serialized == graph.to_json()


def test_graph_rejects_duplicate_node_identity():
    with pytest.raises(CanonicalGraphError, match="node_id must be unique"):
        CanonicalGraph(
            nodes=(SemanticNode("n1", "Party"), SemanticNode("n1", "Customer"))
        )


def test_graph_rejects_duplicate_relationship_identity():
    relationship = lambda: CanonicalRelationship(
        RelationshipInstance("r1", "a", "places", "b")
    )
    with pytest.raises(CanonicalGraphError, match="relationship_id must be unique"):
        CanonicalGraph(relationships=(relationship(), relationship()))


def test_json_serialization_rejects_unsupported_values():
    graph = CanonicalGraph(nodes=(SemanticNode("n1", "Party", {"bad": object()}),))

    with pytest.raises(CanonicalGraphError, match="not JSON-serializable"):
        graph.to_json()
