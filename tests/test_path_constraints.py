import pytest

from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.path_constraints import PathEndsAt, PathConstraintError, evaluate_path_ends_at
from scm_ontology.relationship_identity import RelationshipInstance
from scm_ontology.relation_path_query import RelationPathQuery


def graph() -> CanonicalGraph:
    return CanonicalGraph(
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


def test_path_ends_at_filters_existing_paths() -> None:
    matches = evaluate_path_ends_at(
        graph(),
        RelationPathQuery("product:1", ("supplies", "located_at")),
        PathEndsAt("site:1"),
    )
    assert len(matches) == 1
    assert matches[0].node_ids == ("product:1", "supplier:1", "site:1")


def test_path_ends_at_rejects_empty_node_id() -> None:
    with pytest.raises(PathConstraintError):
        PathEndsAt("")
