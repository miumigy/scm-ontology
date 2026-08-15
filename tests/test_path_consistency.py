import pytest

from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.path_consistency import PathConsistencyError, validate_path_consistency
from scm_ontology.relation_path_query import RelationPathMatch
from scm_ontology.relationship_identity import RelationshipInstance


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


def test_valid_path_has_continuous_endpoints() -> None:
    validate_path_consistency(
        graph(),
        RelationPathMatch(("product:1", "supplier:1", "site:1"), ("rel:1", "rel:2")),
    )


def test_path_rejects_endpoint_discontinuity() -> None:
    with pytest.raises(PathConsistencyError):
        validate_path_consistency(
            graph(),
            RelationPathMatch(("product:1", "site:1", "supplier:1"), ("rel:1", "rel:2")),
        )


def test_path_rejects_unresolved_relationship_identity() -> None:
    with pytest.raises(PathConsistencyError):
        validate_path_consistency(
            graph(),
            RelationPathMatch(("product:1", "supplier:1"), ("rel:missing",)),
        )
