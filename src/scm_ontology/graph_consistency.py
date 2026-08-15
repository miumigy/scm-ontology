from __future__ import annotations

from .canonical_graph import CanonicalGraph


class GraphConsistencyError(ValueError):
    pass


def validate_graph_consistency(graph: CanonicalGraph) -> None:
    """Validate that every relationship endpoint resolves to a graph node."""
    node_ids = {node.node_id for node in graph.nodes}
    for relationship in graph.relationships:
        if relationship.instance.from_id not in node_ids:
            raise GraphConsistencyError(
                f"relationship source does not resolve to a node: {relationship.instance.from_id}"
            )
        if relationship.instance.to_id not in node_ids:
            raise GraphConsistencyError(
                f"relationship target does not resolve to a node: {relationship.instance.to_id}"
            )
