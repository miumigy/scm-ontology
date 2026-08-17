"""Governance boundary for reasoning outputs."""
from __future__ import annotations

from dataclasses import dataclass

from .governed_query_context import GovernedQueryContext
from .reasoning_output import ReasoningOutput


class ReasoningOutputGovernanceError(ValueError):
    """Raised when a reasoning output cannot be safely governed."""


@dataclass(frozen=True)
class GovernedReasoningOutput:
    """Immutable reasoning result linked to its governed query context."""

    contract_version: str
    context_id: str
    graph_identity: str
    proposal: object
    rationale: str
    evidence_ids: tuple[str, ...]
    provenance_ids: tuple[str, ...]
    confidence: float | None

    def to_mapping(self) -> dict[str, object]:
        return {
            "contract_version": self.contract_version,
            "context_id": self.context_id,
            "graph_identity": self.graph_identity,
            "proposal": self.proposal,
            "rationale": self.rationale,
            "evidence_ids": list(self.evidence_ids),
            "provenance_ids": list(self.provenance_ids),
            "confidence": self.confidence,
        }


def govern_reasoning_output(
    context: GovernedQueryContext,
    output: ReasoningOutput,
) -> GovernedReasoningOutput:
    """Bind a reasoning output to its governed input lineage."""
    if not isinstance(context, GovernedQueryContext):
        raise ReasoningOutputGovernanceError("context must be a GovernedQueryContext")
    if not isinstance(output, ReasoningOutput):
        raise ReasoningOutputGovernanceError("output must be a ReasoningOutput")
    if output.context_id != context.context_id:
        raise ReasoningOutputGovernanceError("reasoning output context_id does not match governed context")

    allowed_evidence = set(context.evidence_ids)
    allowed_provenance = set(context.provenance_ids)
    if not set(output.evidence_ids).issubset(allowed_evidence):
        raise ReasoningOutputGovernanceError("reasoning output references evidence outside the governed context")
    if not set(output.provenance_ids).issubset(allowed_provenance):
        raise ReasoningOutputGovernanceError("reasoning output references provenance outside the governed context")
    if not context.graph_identity.startswith("sha256:"):
        raise ReasoningOutputGovernanceError("governed context has an invalid graph identity")

    return GovernedReasoningOutput(
        contract_version="S359.1",
        context_id=context.context_id,
        graph_identity=context.graph_identity,
        proposal=output.proposal,
        rationale=output.rationale,
        evidence_ids=tuple(sorted(output.evidence_ids)),
        provenance_ids=tuple(sorted(output.provenance_ids)),
        confidence=output.confidence,
    )
