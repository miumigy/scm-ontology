import pytest

from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.relation_path_query import (
    RelationPathQuery,
    RelationPathQueryError,
    query_relation_paths,
)
from scm_ontology.relationship_identity import RelationshipInstance


def test_relation_path_query_finds_exact_predicate_sequence() -> None:
    graph = CanonicalGraph(
        nodes=(
            SemanticNode("product:1", "Product"),
            SemanticNode("supplier:1", "Supplier"),
            SemanticNode("site:1", "Site"),
        ),
        relationships=(
            CanonicalRelationship(RelationshipInstance("rel:1", "product:1", "supplies", "supplier:1")),
            CanonicalRelationship(RelationshipInstance("rel:2", "supplier:1", "located_at", "site:1")),
        ),
    )
    matches = query_relation_paths(
        graph,
        RelationPathQuery("product:1", ("supplies", "located_at")),
    )
    assert matches[0].node_ids == ("product:1", "supplier:1", "site:1")
    assert matches[0].relationship_ids == ("rel:1", "rel:2")


def test_relation_path_query_rejects_unknown_start_node() -> None:
    graph = CanonicalGraph(nodes=(SemanticNode("product:1", "Product"),))
    with pytest.raises(RelationPathQueryError):
        query_relation_paths(graph, RelationPathQuery("missing", ("supplies",)))
