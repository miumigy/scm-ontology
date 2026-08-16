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

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "CanonicalGraph":
        """Construct a graph from the canonical mapping representation.

        Relationship mappings accept both the current flat representation
        emitted by ``to_mapping`` and the historical ``instance`` wrapper used
        by early fixtures. Supporting the latter keeps persisted fixtures
        readable while the canonical output remains normalized.
        """
        if not isinstance(value, Mapping):
            raise CanonicalGraphError("graph mapping must be a mapping")

        try:
            nodes = tuple(
                SemanticNode(
                    node_id=node["id"],
                    node_type=node.get("type", node.get("node_type", "")),
                    properties=node.get("properties", {}),
                )
                for node in value.get("nodes", ())
            )
            relationships: list[CanonicalRelationship] = []
            for raw in value.get("relationships", ()):
                instance_data = raw.get("instance", raw)
                instance = RelationshipInstance(
                    relationship_id=instance_data["relationship_id"] if "relationship_id" in instance_data else instance_data["id"],
                    from_id=instance_data["from_id"] if "from_id" in instance_data else instance_data["from"],
                    predicate=instance_data["predicate"],
                    to_id=instance_data["to_id"] if "to_id" in instance_data else instance_data["to"],
                )
                versions = tuple(
                    RelationshipVersion(
                        valid_from=version["valid_from"],
                        valid_to=version.get("valid_to"),
                        qualifiers=version.get("qualifiers"),
                    )
                    for version in raw.get("versions", ())
                )
                relationships.append(CanonicalRelationship(instance, versions))
        except (KeyError, TypeError, AttributeError) as exc:
            raise CanonicalGraphError(f"invalid canonical graph mapping: {exc}") from exc

        return cls(nodes=nodes, relationships=tuple(relationships))

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
