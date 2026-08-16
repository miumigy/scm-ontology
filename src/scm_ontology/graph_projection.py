"""Deterministic graph projection of canonical records.

S337 defines a projection boundary only. It does not mutate a graph store,
perform identity resolution, or infer relationships.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any


class GraphProjectionError(ValueError):
    """Raised when a graph projection violates the canonical contract."""


@dataclass(frozen=True)
class GraphNode:
    node_id: str
    node_type: str
    properties: tuple[tuple[str, Any], ...] = ()

    def __post_init__(self) -> None:
        if not self.node_id.strip() or not self.node_type.strip():
            raise GraphProjectionError("node_id and node_type must be non-empty")

    def to_mapping(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "properties": dict(self.properties),
        }


@dataclass(frozen=True)
class GraphRelationship:
    relationship_id: str
    relationship_type: str
    source_node_id: str
    target_node_id: str
    properties: tuple[tuple[str, Any], ...] = ()

    def __post_init__(self) -> None:
        if not all(
            (
                self.relationship_id.strip(),
                self.relationship_type.strip(),
                self.source_node_id.strip(),
                self.target_node_id.strip(),
            )
        ):
            raise GraphProjectionError(
                "relationship identifiers and type must be non-empty"
            )

    def to_mapping(self) -> dict[str, Any]:
        return {
            "relationship_id": self.relationship_id,
            "relationship_type": self.relationship_type,
            "source_node_id": self.source_node_id,
            "target_node_id": self.target_node_id,
            "properties": dict(self.properties),
        }


@dataclass(frozen=True)
class GraphProjection:
    nodes: tuple[GraphNode, ...] = ()
    relationships: tuple[GraphRelationship, ...] = ()
    provenance_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        node_ids = [node.node_id for node in self.nodes]
        if len(node_ids) != len(set(node_ids)):
            raise GraphProjectionError("duplicate node_id")

        relationship_ids = [rel.relationship_id for rel in self.relationships]
        if len(relationship_ids) != len(set(relationship_ids)):
            raise GraphProjectionError("duplicate relationship_id")

        known = set(node_ids)
        if any(
            rel.source_node_id not in known or rel.target_node_id not in known
            for rel in self.relationships
        ):
            raise GraphProjectionError(
                "relationship endpoint must reference a projected node"
            )

        object.__setattr__(
            self,
            "provenance_ids",
            tuple(sorted(set(self.provenance_ids))),
        )

    def to_mapping(self) -> dict[str, Any]:
        return {
            "contract_version": "S337.1",
            "nodes": [
                node.to_mapping()
                for node in sorted(self.nodes, key=lambda item: item.node_id)
            ],
            "relationships": [
                relationship.to_mapping()
                for relationship in sorted(
                    self.relationships, key=lambda item: item.relationship_id
                )
            ],
            "provenance_ids": list(self.provenance_ids),
        }


def graph_projection_to_json(projection: GraphProjection) -> str:
    """Serialize the projection deterministically while preserving UTF-8."""
    return json.dumps(
        projection.to_mapping(),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
