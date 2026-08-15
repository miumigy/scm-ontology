import pytest

from scm_ontology.canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from scm_ontology.path_constraints import (
    PathContainsNode,
    PathContainsPredicate,
    PathEndsAt,
    evaluate_path_contains_node,
    evaluate_path_contains_predicate,
    evaluate_path_ends_at,
)
from scm_ontology.relation_path_query import RelationPathQuery
from scm_ontology.relationship_identity import RelationshipInstance


def graph() -> CanonicalGraph:
    return CanonicalGraph(
        nodes=(SemanticNode("product:1", "Product"), SemanticNode("supplier:1", "Supplier"), SemanticNode("site:1", "Site")),
        relationships=(
            CanonicalRelationship(RelationshipInstance("rel:1", "product:1", "supplies", "supplier:1")),
            CanonicalRelationship(RelationshipInstance("rel:2", "supplier:1", "located_at", "site:1")),
        ),
    )


def query() -> RelationPathQuery:
    return RelationPathQuery("product:1", ("supplies", "located_at"))


def test_contains_node() -> None:
    matches = evaluate_path_contains_node(graph(), query(), PathContainsNode("supplier:1"))
    assert len(matches) == 1


def test_contains_predicate() -> None:
    matches = evaluate_path_contains_predicate(graph(), query(), PathContainsPredicate("located_at"))
    assert len(matches) == 1


def test_ends_at_remains_supported() -> None:
    matches = evaluate_path_ends_at(graph(), query(), PathEndsAt("site:1"))
    assert len(matches) == 1
