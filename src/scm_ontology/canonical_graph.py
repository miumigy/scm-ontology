"""Canonical graph representation and deterministic JSON serialization.

This module defines a transport-neutral canonical graph contract. JSON is used
only as a serialization format; the ontology itself does not depend on JSON,
RDF, OWL, or a graph database schema.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any, Mapping

from .relationship_identity import RelationshipInstance
from .relationship_version import RelationshipVersion


class CanonicalGraphError(ValueError):
    """Raised when a canonical graph cannot be represented safely."""


@dataclass(frozen=True)
class SemanticNode:
    """A canonical graph node with stable semantic identity and type."""

    node_id: str
    node_type: str
    properties: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.node_id.strip():
            raise CanonicalGraphError("node_id must be non-empty")
        if not self.node_type.strip():
            raise CanonicalGraphError("node_type must be non-empty")
        if not isinstance(self.properties, Mapping):
            raise CanonicalGraphError("properties must be a mapping")


@dataclass(frozen=True)
class CanonicalRelationship:
    """A relationship plus its optional temporal semantic versions."""

    instance: RelationshipInstance
    versions: tuple[RelationshipVersion, ...] = ()

    def to_mapping(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "id": self.instance.relationship_id,
            "from": self.instance.from_id,
            "predicate": self.instance.predicate,
            "to": self.instance.to_id,
        }
        if self.versions:
            result["versions"] = [
                {
                    "valid_from": version.valid_from,
                    "valid_to": version.valid_to,
                    **({"qualifiers": dict(version.qualifiers)} if version.qualifiers is not None else {}),
                }
                for version in self.versions
            ]
        return result


@dataclass(frozen=True)
class CanonicalGraph:
    """A transport-neutral canonical SCM graph."""

    nodes: tuple[SemanticNode, ...] = ()
    relationships: tuple[CanonicalRelationship, ...] = ()

    def __post_init__(self) -> None:
        node_ids = [node.node_id for node in self.nodes]
        if len(node_ids) != len(set(node_ids)):
            raise CanonicalGraphError("node_id must be unique within a graph")
        relationship_ids = [rel.instance.relationship_id for rel in self.relationships]
        if len(relationship_ids) != len(set(relationship_ids)):
            raise CanonicalGraphError("relationship_id must be unique within a graph")

    def to_mapping(self) -> dict[str, Any]:
        """Return the canonical graph document independent of a transport format."""
        return {
            "nodes": [
                {
                    "id": node.node_id,
                    "type": node.node_type,
                    **({"properties": dict(node.properties)} if node.properties else {}),
                }
                for node in self.nodes
            ],
            "relationships": [relationship.to_mapping() for relationship in self.relationships],
        }

    def to_json(self) -> str:
        """Serialize the canonical graph deterministically as JSON."""
        try:
            return json.dumps(
                self.to_mapping(),
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
        except (TypeError, ValueError) as exc:
            raise CanonicalGraphError(f"graph is not JSON-serializable: {exc}") from exc


def is_canonical_graph(value: object) -> bool:
    return isinstance(value, CanonicalGraph)
