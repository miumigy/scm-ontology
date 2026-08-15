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


def evaluate_path_ends_at(
    graph: CanonicalGraph,
    query: RelationPathQuery,
    constraint: PathEndsAt,
) -> tuple[RelationPathMatch, ...]:
    """Return only existing paths whose terminal node matches the constraint."""
    matches = query_relation_paths(graph, query)
    return tuple(match for match in matches if match.node_ids[-1] == constraint.node_id)
