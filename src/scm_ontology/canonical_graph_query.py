"""Deterministic query boundaries for persisted canonical graphs."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .canonical_graph import CanonicalGraph
from .canonical_graph_persistence import CanonicalGraphPersistenceError
from .graph_query import GraphQueryError, GraphQueryResult
from .graph_projection import GraphNode, GraphRelationship


class CanonicalGraphQueryError(ValueError):
    """Raised when a persisted canonical graph query cannot be fulfilled."""


class QueryableCanonicalGraphStore(Protocol):
    def load(self, graph_id: str, *, graph_version: str | None = None) -> CanonicalGraph: ...


@dataclass(frozen=True)
class CanonicalGraphQueryBoundary:
    """Read-only query facade binding persistence selection to graph queries."""

    store: QueryableCanonicalGraphStore

    def nodes(self, graph_id: str, *, graph_version: str | None = None, node_type: str | None = None, node_id: str | None = None) -> GraphQueryResult:
        graph = self._load(graph_id, graph_version)
        try:
            return query_canonical_nodes(graph, node_type=node_type, node_id=node_id)
        except GraphQueryError as exc:
            raise CanonicalGraphQueryError(str(exc)) from exc

    def relationships(self, graph_id: str, *, graph_version: str | None = None, relationship_type: str | None = None, node_id: str | None = None) -> GraphQueryResult:
        graph = self._load(graph_id, graph_version)
        try:
            return query_canonical_relationships(graph, relationship_type=relationship_type, node_id=node_id)
        except GraphQueryError as exc:
            raise CanonicalGraphQueryError(str(exc)) from exc

    def _load(self, graph_id: str, graph_version: str | None) -> CanonicalGraph:
        if not isinstance(graph_id, str) or not graph_id.strip():
            raise CanonicalGraphQueryError("graph_id must be non-empty")
        try:
            return self.store.load(graph_id, graph_version=graph_version)
        except CanonicalGraphPersistenceError as exc:
            raise CanonicalGraphQueryError(str(exc)) from exc


def _validate_filter(name: str, value: str | None) -> None:
    if value is not None and not value.strip():
        raise GraphQueryError(f"{name} must be non-empty when supplied")


def query_canonical_nodes(graph: CanonicalGraph, *, node_type: str | None = None, node_id: str | None = None) -> GraphQueryResult:
    """Query canonical nodes by exact identity/type with deterministic ordering."""
    _validate_filter("node_type", node_type)
    _validate_filter("node_id", node_id)
    nodes = tuple(
        GraphNode(n.node_id, n.node_type, tuple(sorted(n.properties.items())))
        for n in sorted(
            (n for n in graph.nodes if (node_id is None or n.node_id == node_id) and (node_type is None or n.node_type == node_type)),
            key=lambda n: n.node_id,
        )
    )
    ids = {n.node_id for n in nodes}
    relationships = tuple(
        GraphRelationship(r.instance.relationship_id, r.instance.predicate, r.instance.from_id, r.instance.to_id)
        for r in sorted(
            (r for r in graph.relationships if r.instance.from_id in ids and r.instance.to_id in ids),
            key=lambda r: r.instance.relationship_id,
        )
    )
    return GraphQueryResult(nodes, relationships, ())


def query_canonical_relationships(graph: CanonicalGraph, *, relationship_type: str | None = None, node_id: str | None = None) -> GraphQueryResult:
    """Query canonical relationships by exact predicate/endpoint."""
    _validate_filter("relationship_type", relationship_type)
    _validate_filter("node_id", node_id)
    relationships = tuple(
        GraphRelationship(r.instance.relationship_id, r.instance.predicate, r.instance.from_id, r.instance.to_id)
        for r in sorted(
            (r for r in graph.relationships if (relationship_type is None or r.instance.predicate == relationship_type) and (node_id is None or r.instance.from_id == node_id or r.instance.to_id == node_id)),
            key=lambda r: r.instance.relationship_id,
        )
    )
    ids = {r.source_node_id for r in relationships} | {r.target_node_id for r in relationships}
    nodes = tuple(
        GraphNode(n.node_id, n.node_type, tuple(sorted(n.properties.items())))
        for n in sorted((n for n in graph.nodes if n.node_id in ids), key=lambda n: n.node_id)
    )
    return GraphQueryResult(nodes, relationships, ())
