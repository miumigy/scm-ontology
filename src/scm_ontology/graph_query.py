"""Deterministic in-memory query boundary over S337 graph projections."""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any

from .graph_projection import GraphNode, GraphProjection, GraphRelationship


class GraphQueryError(ValueError):
    """Raised when a graph query violates the S338 contract."""


@dataclass(frozen=True)
class GraphQueryResult:
    nodes: tuple[GraphNode, ...] = ()
    relationships: tuple[GraphRelationship, ...] = ()
    provenance_ids: tuple[str, ...] = ()

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "S338.1",
            "nodes": [n.to_mapping() for n in sorted(self.nodes, key=lambda x: x.node_id)],
            "relationships": [r.to_mapping() for r in sorted(self.relationships, key=lambda x: x.relationship_id)],
            "provenance_ids": sorted(set(self.provenance_ids)),
        }


def query_nodes(projection: GraphProjection, *, node_type: str | None = None, node_id: str | None = None) -> GraphQueryResult:
    """Select projected nodes by exact canonical identity/type."""
    if node_id is not None and not node_id.strip():
        raise GraphQueryError("node_id must be non-empty when supplied")
    if node_type is not None and not node_type.strip():
        raise GraphQueryError("node_type must be non-empty when supplied")
    nodes = tuple(n for n in projection.nodes if (node_id is None or n.node_id == node_id) and (node_type is None or n.node_type == node_type))
    ids = {n.node_id for n in nodes}
    rels = tuple(r for r in projection.relationships if r.source_node_id in ids or r.target_node_id in ids)
    return GraphQueryResult(nodes, rels, projection.provenance_ids)


def query_relationships(projection: GraphProjection, *, relationship_type: str | None = None, node_id: str | None = None) -> GraphQueryResult:
    """Select relationships by exact type and/or endpoint node identity."""
    if relationship_type is not None and not relationship_type.strip():
        raise GraphQueryError("relationship_type must be non-empty when supplied")
    if node_id is not None and not node_id.strip():
        raise GraphQueryError("node_id must be non-empty when supplied")
    rels = tuple(r for r in projection.relationships if (relationship_type is None or r.relationship_type == relationship_type) and (node_id is None or r.source_node_id == node_id or r.target_node_id == node_id))
    ids = {r.source_node_id for r in rels} | {r.target_node_id for r in rels}
    nodes = tuple(n for n in projection.nodes if n.node_id in ids)
    return GraphQueryResult(nodes, rels, projection.provenance_ids)


def graph_query_to_json(result: GraphQueryResult) -> str:
    """Serialize an S338 query result deterministically with UTF-8 preserved."""
    return json.dumps(result.to_mapping(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
