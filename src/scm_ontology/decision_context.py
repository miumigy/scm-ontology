"""Governed SCM OS Decision Context boundary.

S333 bundles already-canonical business-question results into an immutable,
read-only context for downstream planning, simulation, optimization, or
reasoning. It does not create or mutate canonical truth.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Iterable


class DecisionContextError(ValueError):
    """Raised when a decision-context input violates the S333 contract."""


@dataclass(frozen=True)
class DecisionObservation:
    """A governed derived observation identified by its semantic question."""

    question_id: str
    value: Any
    evidence_ids: tuple[str, ...] = ()
    provenance_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.question_id.strip():
            raise DecisionContextError("question_id must be non-empty")
        object.__setattr__(self, "evidence_ids", tuple(sorted(set(self.evidence_ids))))
        object.__setattr__(self, "provenance_ids", tuple(sorted(set(self.provenance_ids))))

    def to_mapping(self) -> dict[str, Any]:
        return {
            "question_id": self.question_id,
            "value": self.value,
            "evidence_ids": list(self.evidence_ids),
            "provenance_ids": list(self.provenance_ids),
        }


@dataclass(frozen=True)
class DecisionContext:
    """Immutable collection of explicit derived observations for downstream use."""

    context_id: str
    observations: tuple[DecisionObservation, ...]

    def __post_init__(self) -> None:
        if not self.context_id.strip():
            raise DecisionContextError("context_id must be non-empty")
        question_ids = [o.question_id for o in self.observations]
        if len(question_ids) != len(set(question_ids)):
            raise DecisionContextError("question_id must be unique within a context")
        object.__setattr__(self, "observations", tuple(sorted(self.observations, key=lambda o: o.question_id)))

    def to_mapping(self) -> dict[str, Any]:
        return {
            "context_id": self.context_id,
            "observations": [observation.to_mapping() for observation in self.observations],
        }


def build_decision_context(context_id: str, observations: Iterable[DecisionObservation]) -> DecisionContext:
    """Build a deterministic read-only decision context from explicit observations."""
    return DecisionContext(context_id=context_id, observations=tuple(observations))


def decision_context_to_mapping(context: DecisionContext) -> dict[str, Any]:
    """Return the deterministic JSON-safe S333 mapping."""
    return {"contract_version": "S333.1", **context.to_mapping()}


def decision_context_to_json(context: DecisionContext) -> str:
    """Serialize S333 deterministically with UTF-8 characters preserved."""
    return json.dumps(decision_context_to_mapping(context), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
