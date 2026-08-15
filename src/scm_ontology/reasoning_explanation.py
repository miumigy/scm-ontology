from __future__ import annotations

from dataclasses import dataclass

from .path_reasoning_result import PathReasoningResult


class ReasoningExplanationError(ValueError):
    pass


@dataclass(frozen=True)
class ExplanationStep:
    kind: str
    ref: str
    detail: str | None = None

    def __post_init__(self) -> None:
        if not self.kind.strip():
            raise ReasoningExplanationError("kind must be non-empty")
        if not self.ref.strip():
            raise ReasoningExplanationError("ref must be non-empty")


@dataclass(frozen=True)
class ReasoningExplanation:
    result_ref: str
    steps: tuple[ExplanationStep, ...]

    def __post_init__(self) -> None:
        if not self.result_ref.strip():
            raise ReasoningExplanationError("result_ref must be non-empty")


def explain_path_reasoning(result: PathReasoningResult) -> ReasoningExplanation:
    """Produce a deterministic explanation trace from an existing path result."""
    steps: list[ExplanationStep] = []
    for path_evidence in result.paths:
        path = path_evidence.path
        for relationship_id in path.relationship_ids:
            steps.append(ExplanationStep("relationship", relationship_id))
        for evidence in path_evidence.evidence.refs:
            steps.append(ExplanationStep("evidence", evidence.source_ref))
    if not steps:
        steps.append(ExplanationStep("result", result.status))
    return ReasoningExplanation(result.result_ref, tuple(steps))
