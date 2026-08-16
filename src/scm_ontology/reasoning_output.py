"""Immutable output boundary from reasoning engines into SCM semantics."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class ReasoningOutputError(ValueError):
    """Raised when a reasoning output violates the S343 contract."""


@dataclass(frozen=True)
class ReasoningOutput:
    """A proposed decision result with explicit support metadata."""

    context_id: str
    proposal: Any
    rationale: str
    evidence_ids: tuple[str, ...] = ()
    provenance_ids: tuple[str, ...] = ()
    confidence: float | None = None

    def __post_init__(self) -> None:
        if not self.context_id.strip():
            raise ReasoningOutputError("context_id must be non-empty")
        if not self.rationale.strip():
            raise ReasoningOutputError("rationale must be non-empty")
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise ReasoningOutputError("confidence must be between 0 and 1")
        object.__setattr__(self, "evidence_ids", tuple(sorted(set(self.evidence_ids))))
        object.__setattr__(self, "provenance_ids", tuple(sorted(set(self.provenance_ids))))

    def to_mapping(self) -> dict[str, object]:
        return {
            "contract_version": "S343.1",
            "context_id": self.context_id,
            "proposal": self.proposal,
            "rationale": self.rationale,
            "evidence_ids": list(self.evidence_ids),
            "provenance_ids": list(self.provenance_ids),
            "confidence": self.confidence,
        }
