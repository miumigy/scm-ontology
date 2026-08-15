from __future__ import annotations

from .canonical_graph import CanonicalGraph
from .relation_path_query import RelationPathMatch


class PathConsistencyError(ValueError):
    pass


def validate_path_consistency(
    graph: CanonicalGraph,
    match: RelationPathMatch,
) -> None:
    """Validate endpoint continuity and relationship identity for an existing path."""
    if len(match.node_ids) != len(match.relationship_ids) + 1:
        raise PathConsistencyError("path must contain exactly one more node than relationship")

    relationships = {relationship.instance.relationship_id: relationship.instance for relationship in graph.relationships}
    if len(set(match.relationship_ids)) != len(match.relationship_ids):
        raise PathConsistencyError("path must not repeat a relationship identity")

    for index, relationship_id in enumerate(match.relationship_ids):
        relationship = relationships.get(relationship_id)
        if relationship is None:
            raise PathConsistencyError(f"path relationship does not resolve: {relationship_id}")
        if relationship.from_id != match.node_ids[index] or relationship.to_id != match.node_ids[index + 1]:
            raise PathConsistencyError(f"path endpoint mismatch at relationship: {relationship_id}")
