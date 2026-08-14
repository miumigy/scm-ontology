"""Minimal semantic query primitives over the canonical SCM Graph."""
from __future__ import annotations

from dataclasses import dataclass

from .canonical_graph import CanonicalRelationship, SemanticNode
from .scm_graph import SCMGraph


@dataclass(frozen=True)
class NodeMatch:
    """A node returned by a semantic query."""

    node: SemanticNode


@dataclass(frozen=True)
class RelationshipMatch:
    """A relationship returned by a semantic query."""

    relationship: CanonicalRelationship


class SemanticQuery:
    """Read-only query facade; it retrieves graph facts without inference."""

    def __init__(self, graph: SCMGraph) -> None:
        self._graph = graph

    def nodes(self, *, node_type: str | None = None) -> tuple[NodeMatch, ...]:
        return tuple(
            NodeMatch(node)
            for node in self._graph.canonical.nodes
            if node_type is None or node.node_type == node_type
        )

    def relationships(
        self,
        *,
        predicate: str | None = None,
        from_id: str | None = None,
        to_id: str | None = None,
    ) -> tuple[RelationshipMatch, ...]:
        return tuple(
            RelationshipMatch(rel)
            for rel in self._graph.canonical.relationships
            if (predicate is None or rel.instance.predicate == predicate)
            and (from_id is None or rel.instance.from_id == from_id)
            and (to_id is None or rel.instance.to_id == to_id)
        )

    def neighbors(
        self,
        node_id: str,
        *,
        predicate: str | None = None,
        direction: str = "out",
    ) -> tuple[NodeMatch, ...]:
        return tuple(
            NodeMatch(node)
            for node in self._graph.related(node_id, predicate=predicate, direction=direction)
        )

    def fact_count(self) -> int:
        """Return the number of canonical graph facts represented by nodes and relationships."""
        return len(self._graph.canonical.nodes) + len(self._graph.canonical.relationships)
