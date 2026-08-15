from __future__ import annotations

from dataclasses import dataclass

from .canonical_graph import CanonicalGraph, SemanticNode
from .graph_consistency import validate_graph_consistency


class ReasoningQueryError(ValueError):
    pass


@dataclass(frozen=True)
class NodeQuery:
    node_type: str | None = None
    node_id: str | None = None


def query_nodes(graph: CanonicalGraph, query: NodeQuery = NodeQuery()) -> tuple[SemanticNode, ...]:
    """Return canonical graph nodes matching an explicit reasoning query."""
    validate_graph_consistency(graph)
    if query.node_type is None and query.node_id is None:
        raise ReasoningQueryError("at least one query constraint is required")
    return tuple(
        node
        for node in graph.nodes
        if (query.node_type is None or node.node_type == query.node_type)
        and (query.node_id is None or node.node_id == query.node_id)
    )
