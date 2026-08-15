from __future__ import annotations

from dataclasses import dataclass


class ReasoningConfidenceError(ValueError):
    pass


@dataclass(frozen=True)
class ConfidenceFactors:
    evidence_completeness: float
    source_agreement: float
    path_consistency: float
    determinism: float

    def __post_init__(self) -> None:
        values = (
            self.evidence_completeness,
            self.source_agreement,
            self.path_consistency,
            self.determinism,
        )
        if any(not 0.0 <= value <= 1.0 for value in values):
            raise ReasoningConfidenceError("confidence factors must be between 0 and 1")


@dataclass(frozen=True)
class ReasoningConfidence:
    score: float
    factors: ConfidenceFactors

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ReasoningConfidenceError("confidence score must be between 0 and 1")


def calculate_reasoning_confidence(factors: ConfidenceFactors) -> ReasoningConfidence:
    """Calculate a transparent confidence score as the arithmetic mean of factors."""
    values = (
        factors.evidence_completeness,
        factors.source_agreement,
        factors.path_consistency,
        factors.determinism,
    )
    return ReasoningConfidence(sum(values) / len(values), factors)
