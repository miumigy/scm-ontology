"""Read-only deterministic query adapter for CanonicalGraph.

S356 bridges the canonical graph contract to the existing graph query result
contract without changing the projection/query implementation.
"""
from __future__ import annotations

from .canonical_graph import CanonicalGraph
from .graph_query import GraphQueryError, GraphQueryResult
from .graph_projection import GraphNode, GraphRelationship


def _validate_filter(name: str, value: str | None) -> None:
    if value is not None and not value.strip():
        raise GraphQueryError(f"{name} must be non-empty when supplied")


def query_canonical_nodes(
    graph: CanonicalGraph,
    *,
    node_type: str | None = None,
    node_id: str | None = None,
) -> GraphQueryResult:
    """Query CanonicalGraph nodes by exact identity/type.

    Results are sorted by canonical node identity and include only relationships
    incident to the selected nodes.
    """
    _validate_filter("node_type", node_type)
    _validate_filter("node_id", node_id)
    nodes = tuple(
        GraphNode(n.node_id, n.node_type, tuple(sorted(n.properties.items())))
        for n in sorted(
            (n for n in graph.nodes
             if (node_id is None or n.node_id == node_id)
             and (node_type is None or n.node_type == node_type)),
            key=lambda n: n.node_id,
        )
    )
    ids = {n.node_id for n in nodes}
    relationships = tuple(
        GraphRelationship(
            r.instance.relationship_id,
            r.instance.predicate,
            r.instance.from_id,
            r.instance.to_id,
        )
        for r in sorted(
            (r for r in graph.relationships
             if r.instance.from_id in ids or r.instance.to_id in ids),
            key=lambda r: r.instance.relationship_id,
        )
    )
    return GraphQueryResult(nodes, relationships, ())


def query_canonical_relationships(
    graph: CanonicalGraph,
    *,
    relationship_type: str | None = None,
    node_id: str | None = None,
) -> GraphQueryResult:
    """Query CanonicalGraph relationships by exact predicate/endpoint."""
    _validate_filter("relationship_type", relationship_type)
    _validate_filter("node_id", node_id)
    relationships = tuple(
        GraphRelationship(
            r.instance.relationship_id,
            r.instance.predicate,
            r.instance.from_id,
            r.instance.to_id,
        )
        for r in sorted(
            (r for r in graph.relationships
             if (relationship_type is None or r.instance.predicate == relationship_type)
             and (node_id is None or r.instance.from_id == node_id or r.instance.to_id == node_id)),
            key=lambda r: r.instance.relationship_id,
        )
    )
    ids = {r.source_node_id for r in relationships} | {r.target_node_id for r in relationships}
    nodes = tuple(
        GraphNode(n.node_id, n.node_type, tuple(sorted(n.properties.items())))
        for n in sorted((n for n in graph.nodes if n.node_id in ids), key=lambda n: n.node_id)
    )
    return GraphQueryResult(nodes, relationships, ())
