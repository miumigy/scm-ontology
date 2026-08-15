from __future__ import annotations

from dataclasses import dataclass

from .canonical_graph import CanonicalGraph
from .relation_path_query import RelationPathMatch, RelationPathQuery, query_relation_paths


class PathConstraintError(ValueError):
    pass


@dataclass(frozen=True)
class PathEndsAt:
    node_id: str

    def __post_init__(self) -> None:
        if not self.node_id.strip():
            raise PathConstraintError("node_id must be non-empty")


@dataclass(frozen=True)
class PathContainsNode:
    node_id: str

    def __post_init__(self) -> None:
        if not self.node_id.strip():
            raise PathConstraintError("node_id must be non-empty")


@dataclass(frozen=True)
class PathContainsPredicate:
    predicate_ref: str

    def __post_init__(self) -> None:
        if not self.predicate_ref.strip():
            raise PathConstraintError("predicate_ref must be non-empty")


def evaluate_path_ends_at(graph: CanonicalGraph, query: RelationPathQuery, constraint: PathEndsAt) -> tuple[RelationPathMatch, ...]:
    return tuple(match for match in query_relation_paths(graph, query) if match.node_ids[-1] == constraint.node_id)


def evaluate_path_contains_node(graph: CanonicalGraph, query: RelationPathQuery, constraint: PathContainsNode) -> tuple[RelationPathMatch, ...]:
    return tuple(match for match in query_relation_paths(graph, query) if constraint.node_id in match.node_ids)


def evaluate_path_contains_predicate(graph: CanonicalGraph, query: RelationPathQuery, constraint: PathContainsPredicate) -> tuple[RelationPathMatch, ...]:
    predicates = {relationship.instance.relationship_id: relationship.instance.predicate for relationship in graph.relationships}
    return tuple(
        match for match in query_relation_paths(graph, query)
        if any(predicates.get(relationship_id) == constraint.predicate_ref for relationship_id in match.relationship_ids)
    )
