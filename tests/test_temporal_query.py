from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.relationship_identity import RelationshipInstance
from scm_ontology.relationship_version import RelationshipVersion
from scm_ontology.temporal_query import relationships_at


def test_relationships_at_selects_half_open_temporal_version() -> None:
    relationship = CanonicalRelationship(
        RelationshipInstance("r-1", "p-1", "supplies", "f-1"),
        (
            RelationshipVersion("2026-01-01T00:00:00Z", "2026-07-01T00:00:00Z", {"lane": "A"}),
            RelationshipVersion("2026-07-01T00:00:00Z", None, {"lane": "B"}),
        ),
    )
    graph = CanonicalGraph(
        nodes=(SemanticNode("p-1", "Product"), SemanticNode("f-1", "Facility")),
        relationships=(relationship,),
    )

    first = relationships_at(graph, "2026-06-30T12:00:00Z", predicate="supplies")
    second = relationships_at(graph, "2026-07-01T00:00:00Z", predicate="supplies")

    assert first[0].version_index == 0
    assert first[0].qualifiers == {"lane": "A"}
    assert second[0].version_index == 1
    assert second[0].qualifiers == {"lane": "B"}
