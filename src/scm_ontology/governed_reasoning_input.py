"""Deterministic adapter from governed graph-query context to ReasoningInput."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .decision_context import DecisionObservation
from .governed_query_context import GovernedQueryContext
from .reasoning_input import ReasoningInput


class GovernedReasoningInputError(ValueError):
    """Raised when a governed query context cannot cross the reasoning boundary."""


@dataclass(frozen=True)
class GovernedQueryObservation:
    """Stable observation payload carrying query identity and graph lineage."""

    question_id: str
    graph_identity: str
    operation: str
    node_ids: tuple[str, ...]
    relationship_ids: tuple[str, ...]

    def to_value(self) -> dict[str, Any]:
        return {
            "graph_identity": self.graph_identity,
            "operation": self.operation,
            "node_ids": list(self.node_ids),
            "relationship_ids": list(self.relationship_ids),
        }


def build_reasoning_input_from_governed_query_context(
    context: GovernedQueryContext,
) -> ReasoningInput:
    """Convert an immutable governed query context into the existing reasoning contract."""
    if not isinstance(context, GovernedQueryContext):
        raise GovernedReasoningInputError("context must be a GovernedQueryContext")
    if not context.context_id.strip():
        raise GovernedReasoningInputError("context_id must be non-empty")
    if not context.graph_identity.startswith("sha256:"):
        raise GovernedReasoningInputError("graph_identity must be a sha256 identity")

    observation = GovernedQueryObservation(
        question_id=f"graph_query:{context.query.operation}",
        graph_identity=context.graph_identity,
        operation=context.query.operation,
        node_ids=tuple(sorted(context.node_ids)),
        relationship_ids=tuple(sorted(context.relationship_ids)),
    )
    return ReasoningInput(
        context_id=context.context_id,
        observations=(
            DecisionObservation(
                question_id=observation.question_id,
                value=observation.to_value(),
                evidence_ids=tuple(sorted(context.evidence_ids)),
                provenance_ids=tuple(sorted(context.provenance_ids)),
            ),
        ),
        evidence_ids=tuple(sorted(context.evidence_ids)),
        provenance_ids=tuple(sorted(context.provenance_ids)),
    )
