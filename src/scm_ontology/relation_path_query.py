from __future__ import annotations

from dataclasses import dataclass

from .canonical_graph import CanonicalGraph
from .graph_consistency import validate_graph_consistency


class RelationPathQueryError(ValueError):
    pass


@dataclass(frozen=True)
class RelationPathQuery:
    start_node_id: str
    predicates: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.start_node_id.strip():
            raise RelationPathQueryError("start_node_id must be non-empty")
        if not self.predicates or any(not predicate.strip() for predicate in self.predicates):
            raise RelationPathQueryError("predicates must contain at least one non-empty predicate")


@dataclass(frozen=True)
class RelationPathMatch:
    node_ids: tuple[str, ...]
    relationship_ids: tuple[str, ...]


def query_relation_paths(
    graph: CanonicalGraph,
    query: RelationPathQuery,
) -> tuple[RelationPathMatch, ...]:
    """Find exact predicate-sequence paths from a canonical start node."""
    validate_graph_consistency(graph)
    node_ids = {node.node_id for node in graph.nodes}
    if query.start_node_id not in node_ids:
        raise RelationPathQueryError(f"start node does not resolve: {query.start_node_id}")

    matches: list[RelationPathMatch] = []

    def walk(current_id: str, depth: int, nodes: tuple[str, ...], relationships: tuple[str, ...]) -> None:
        if depth == len(query.predicates):
            matches.append(RelationPathMatch(nodes, relationships))
            return
        predicate = query.predicates[depth]
        for relationship in graph.relationships:
            instance = relationship.instance
            if instance.from_id == current_id and instance.predicate == predicate:
                walk(
                    instance.to_id,
                    depth + 1,
                    nodes + (instance.to_id,),
                    relationships + (instance.relationship_id,),
                )

    walk(query.start_node_id, 0, (query.start_node_id,), ())
    return tuple(matches)
