"""Governed projection from canonical graph query results into reasoning observations.

S366 bridges the canonical graph query boundary and the existing immutable
DecisionContext/ReasoningInput contracts. It never infers business meaning:
callers must supply the semantic question id and the queried graph result.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .decision_context import DecisionObservation
from .graph_projection import GraphProjection
from .graph_query import GraphQueryResult


class GraphReasoningProjectionError(ValueError):
    """Raised when a graph-to-reasoning projection violates its contract."""


@dataclass(frozen=True)
class GraphReasoningObservation:
    """Immutable, deterministic observation payload derived from a graph query."""

    question_id: str
    value: dict[str, Any]
    evidence_ids: tuple[str, ...] = ()
    provenance_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.question_id.strip():
            raise GraphReasoningProjectionError("question_id must be non-empty")
        object.__setattr__(self, "evidence_ids", tuple(sorted(set(self.evidence_ids))))
        object.__setattr__(self, "provenance_ids", tuple(sorted(set(self.provenance_ids))))

    def to_decision_observation(self) -> DecisionObservation:
        return DecisionObservation(
            question_id=self.question_id,
            value=self.value,
            evidence_ids=self.evidence_ids,
            provenance_ids=self.provenance_ids,
        )


def project_query_result_to_observation(
    query_result: GraphQueryResult,
    *,
    question_id: str,
    evidence_ids: tuple[str, ...] = (),
    provenance_ids: tuple[str, ...] = (),
) -> GraphReasoningObservation:
    """Convert a deterministic graph query result into one reasoning observation."""
    if not isinstance(query_result, GraphQueryResult):
        raise GraphReasoningProjectionError("query_result must be a GraphQueryResult")
    if not question_id.strip():
        raise GraphReasoningProjectionError("question_id must be non-empty")

    nodes = tuple(sorted(query_result.nodes, key=lambda node: node.node_id))
    relationships = tuple(
        sorted(query_result.relationships, key=lambda relationship: relationship.relationship_id)
    )
    value = {
        "nodes": [node.to_mapping() for node in nodes],
        "relationships": [relationship.to_mapping() for relationship in relationships],
    }
    return GraphReasoningObservation(
        question_id=question_id,
        value=value,
        evidence_ids=evidence_ids,
        provenance_ids=tuple(provenance_ids) + query_result.provenance_ids,
    )


def project_graph_to_observation(
    projection: GraphProjection,
    *,
    question_id: str,
    evidence_ids: tuple[str, ...] = (),
    provenance_ids: tuple[str, ...] = (),
) -> GraphReasoningObservation:
    """Project an already-validated canonical graph projection to one observation."""
    if not isinstance(projection, GraphProjection):
        raise GraphReasoningProjectionError("projection must be a GraphProjection")
    return GraphReasoningObservation(
        question_id=question_id,
        value=projection.to_mapping(),
        evidence_ids=evidence_ids,
        provenance_ids=tuple(provenance_ids) + projection.provenance_ids,
    )
