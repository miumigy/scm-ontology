import pytest

from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.graph_consistency import GraphConsistencyError, validate_graph_consistency
from scm_ontology.relationship_identity import RelationshipInstance


def test_graph_with_resolved_relationship_endpoints_is_consistent() -> None:
    graph = CanonicalGraph(
        nodes=(SemanticNode("entity:1", "Product"), SemanticNode("entity:2", "Site")),
        relationships=(
            CanonicalRelationship(
                RelationshipInstance("rel:1", "entity:1", "stored_at", "entity:2")
            ),
        ),
    )
    validate_graph_consistency(graph)


def test_graph_rejects_dangling_relationship_endpoint() -> None:
    graph = CanonicalGraph(
        nodes=(SemanticNode("entity:1", "Product"),),
        relationships=(
            CanonicalRelationship(
                RelationshipInstance("rel:1", "entity:1", "stored_at", "entity:missing")
            ),
        ),
    )
    with pytest.raises(GraphConsistencyError):
        validate_graph_consistency(graph)
