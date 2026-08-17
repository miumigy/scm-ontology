"""Read-only projection of canonical event lineage into a canonical graph."""
from __future__ import annotations

from dataclasses import dataclass

from .canonical_event_lineage import CanonicalEventLineage
from .canonical_graph import CanonicalGraph, CanonicalRelationship, SemanticNode
from .relationship_identity import RelationshipInstance


class LineageGraphProjectionError(ValueError):
    """Raised when lineage cannot be projected safely."""


@dataclass(frozen=True)
class LineageGraph:
    """Immutable wrapper for a projected lineage graph."""

    graph: CanonicalGraph

    def __post_init__(self) -> None:
        if not isinstance(self.graph, CanonicalGraph):
            raise LineageGraphProjectionError("graph must be a CanonicalGraph")


def _relationship_id(predicate: str, from_id: str, to_id: str) -> str:
    return f"{predicate}:{from_id}:{to_id}"


def build_lineage_graph(lineage: CanonicalEventLineage) -> LineageGraph:
    """Project immutable event lineage into a deterministic lineage graph."""
    if not isinstance(lineage, CanonicalEventLineage):
        raise LineageGraphProjectionError("lineage must be a CanonicalEventLineage")

    nodes = [SemanticNode(node_id=lineage.event_id, node_type="CanonicalEvent")]
    relationships: list[CanonicalRelationship] = []

    for evidence_id in lineage.evidence_ids:
        nodes.append(SemanticNode(node_id=evidence_id, node_type="Evidence"))
        relationships.append(
            CanonicalRelationship(
                RelationshipInstance(
                    relationship_id=_relationship_id(
                        "evidence_for", evidence_id, lineage.event_id
                    ),
                    from_id=evidence_id,
                    predicate="evidence_for",
                    to_id=lineage.event_id,
                )
            )
        )

    for provenance_id in lineage.provenance_ids:
        nodes.append(SemanticNode(node_id=provenance_id, node_type="Provenance"))
        relationships.append(
            CanonicalRelationship(
                RelationshipInstance(
                    relationship_id=_relationship_id(
                        "provenance_for", provenance_id, lineage.event_id
                    ),
                    from_id=provenance_id,
                    predicate="provenance_for",
                    to_id=lineage.event_id,
                )
            )
        )

    return LineageGraph(
        CanonicalGraph(nodes=tuple(nodes), relationships=tuple(relationships))
    )
