from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical_graph import CanonicalGraph
from .reasoning_query import NodeQuery, query_nodes


class SemanticConstraintError(ValueError):
    pass


@dataclass(frozen=True)
class PropertyEquals:
    key: str
    expected: Any


def evaluate_property_equals(
    graph: CanonicalGraph,
    query: NodeQuery,
    constraint: PropertyEquals,
) -> tuple[str, ...]:
    """Return node identities satisfying an explicit property-equality constraint."""
    if not constraint.key.strip():
        raise SemanticConstraintError("constraint property key must be non-empty")
    return tuple(
        node.node_id
        for node in query_nodes(graph, query)
        if node.properties.get(constraint.key) == constraint.expected
    )
