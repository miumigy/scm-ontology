"""Minimal in-memory SCM Graph built on the canonical graph model."""
from __future__ import annotations

from dataclasses import dataclass

from .canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from .relationship_identity import RelationshipInstance


class SCMGraphError(ValueError):
    """Raised when an SCM Graph operation violates graph identity rules."""


@dataclass(frozen=True)
class SCMGraph:
    """Dependency-light graph facade for canonical SCM graph traversal.

    The graph stores canonical nodes and relationships in immutable tuples.
    It is an execution layer, not a persistence or graph-database schema.
    """

    canonical: CanonicalGraph = CanonicalGraph()

    def add_node(self, node: SemanticNode) -> "SCMGraph":
        if any(existing.node_id == node.node_id for existing in self.canonical.nodes):
            raise SCMGraphError(f"node already exists: {node.node_id}")
        return SCMGraph(CanonicalGraph(self.canonical.nodes + (node,), self.canonical.relationships))

    def add_relationship(self, relationship: CanonicalRelationship) -> "SCMGraph":
        if any(existing.instance.relationship_id == relationship.instance.relationship_id for existing in self.canonical.relationships):
            raise SCMGraphError(f"relationship already exists: {relationship.instance.relationship_id}")
        node_ids = {node.node_id for node in self.canonical.nodes}
        if relationship.instance.from_id not in node_ids:
            raise SCMGraphError(f"unknown from node: {relationship.instance.from_id}")
        if relationship.instance.to_id not in node_ids:
            raise SCMGraphError(f"unknown to node: {relationship.instance.to_id}")
        return SCMGraph(CanonicalGraph(self.canonical.nodes, self.canonical.relationships + (relationship,)))

    def node(self, node_id: str) -> SemanticNode | None:
        return next((node for node in self.canonical.nodes if node.node_id == node_id), None)

    def relationship(self, relationship_id: str) -> CanonicalRelationship | None:
        return next((rel for rel in self.canonical.relationships if rel.instance.relationship_id == relationship_id), None)

    def related(self, node_id: str, *, predicate: str | None = None, direction: str = "out") -> tuple[SemanticNode, ...]:
        """Return adjacent nodes filtered by predicate and direction."""
        if direction not in {"out", "in", "both"}:
            raise SCMGraphError("direction must be 'out', 'in', or 'both'")
        ids: list[str] = []
        for rel in self.canonical.relationships:
            instance: RelationshipInstance = rel.instance
            matches: list[str] = []
            if direction in {"out", "both"} and instance.from_id == node_id:
                matches.append(instance.to_id)
            if direction in {"in", "both"} and instance.to_id == node_id:
                matches.append(instance.from_id)
            if predicate is not None and instance.predicate != predicate:
                matches = []
            ids.extend(matches)
        return tuple(node for node in self.canonical.nodes if node.node_id in ids)

    def relationships_from(self, node_id: str, *, predicate: str | None = None) -> tuple[CanonicalRelationship, ...]:
        return tuple(rel for rel in self.canonical.relationships if rel.instance.from_id == node_id and (predicate is None or rel.instance.predicate == predicate))

    def relationships_to(self, node_id: str, *, predicate: str | None = None) -> tuple[CanonicalRelationship, ...]:
        return tuple(rel for rel in self.canonical.relationships if rel.instance.to_id == node_id and (predicate is None or rel.instance.predicate == predicate))

    def to_canonical(self) -> CanonicalGraph:
        return self.canonical

    def to_json(self) -> str:
        return self.canonical.to_json()


def empty_scm_graph() -> SCMGraph:
    """Create an empty SCM Graph."""
    return SCMGraph()
