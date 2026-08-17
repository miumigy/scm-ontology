"""Canonical graph nodes and relationships for evidence/provenance lineage."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical_event_lineage import CanonicalEventLineage
from .canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from .relationship_identity import RelationshipInstance


class LineageGraphError(ValueError):
    """Raised when evidence/provenance graph lineage is invalid."""


@dataclass(frozen=True)
class LineageGraph:
    """Immutable evidence/provenance nodes and their links to one event."""

    graph: CanonicalGraph

    def to_mapping(self) -> dict[str, Any]:
        return self.graph.to_mapping()


def build_lineage_graph(lineage: CanonicalEventLineage) -> LineageGraph:
    """Project S349 lineage into canonical graph nodes without persistence or side effects."""
    if not isinstance(lineage, CanonicalEventLineage):
        raise LineageGraphError("lineage must be a CanonicalEventLineage")

    nodes = [SemanticNode(lineage.event_id, "CanonicalEvent")]
    relationships: list[CanonicalRelationship] = []

    for evidence_id in lineage.evidence_ids:
        nodes.append(SemanticNode(evidence_id, "Evidence"))
        relationships.append(
            CanonicalRelationship(
                RelationshipInstance(
                    relationship_id=f"evidence_for:{evidence_id}:{lineage.event_id}",
                    from_id=evidence_id,
                    predicate="evidence_for",
                    to_id=lineage.event_id,
                )
            )
        )

    for provenance_id in lineage.provenance_ids:
        nodes.append(SemanticNode(provenance_id, "Provenance"))
        relationships.append(
            CanonicalRelationship(
                RelationshipInstance(
                    relationship_id=f"provenance_for:{provenance_id}:{lineage.event_id}",
                    from_id=provenance_id,
                    predicate="provenance_for",
                    to_id=lineage.event_id,
                )
            )
        )

    return LineageGraph(CanonicalGraph(nodes=tuple(nodes), relationships=tuple(relationships)))
