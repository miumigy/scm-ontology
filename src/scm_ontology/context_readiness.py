"""Validate whether a DecisionContext is ready for downstream reasoning."""
from __future__ import annotations

from dataclasses import dataclass

from .decision_context import DecisionContext


class ContextReadinessError(ValueError):
    """Raised when a context violates readiness requirements."""


@dataclass(frozen=True)
class ContextReadiness:
    ready: bool
    context_id: str
    observation_count: int
    missing_evidence_questions: tuple[str, ...] = ()
    missing_provenance_questions: tuple[str, ...] = ()

    def to_mapping(self) -> dict[str, object]:
        return {
            "contract_version": "S341.1",
            "ready": self.ready,
            "context_id": self.context_id,
            "observation_count": self.observation_count,
            "missing_evidence_questions": list(self.missing_evidence_questions),
            "missing_provenance_questions": list(self.missing_provenance_questions),
        }


def validate_context_readiness(context: DecisionContext) -> ContextReadiness:
    """Return deterministic readiness status without mutating the context."""
    missing_evidence = tuple(o.question_id for o in context.observations if not o.evidence_ids)
    missing_provenance = tuple(o.question_id for o in context.observations if not o.provenance_ids)
    return ContextReadiness(
        ready=bool(context.observations) and not missing_evidence and not missing_provenance,
        context_id=context.context_id,
        observation_count=len(context.observations),
        missing_evidence_questions=missing_evidence,
        missing_provenance_questions=missing_provenance,
    )


def require_context_ready(context: DecisionContext) -> DecisionContext:
    """Fail closed unless the context satisfies S341 readiness requirements."""
    status = validate_context_readiness(context)
    if not status.ready:
        raise ContextReadinessError(
            f"DecisionContext {context.context_id!r} is not ready for downstream reasoning"
        )
    return context
