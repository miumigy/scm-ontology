from __future__ import annotations

from dataclasses import dataclass

from .path_reasoning_result import PathReasoningResult
from .reasoning_policy import ReasoningPolicy, TruthClass, validate_graph_mutation, validate_truth_transition


class ReasoningConformanceError(ValueError):
    pass


@dataclass(frozen=True)
class ConformanceReport:
    result_ref: str
    canonical_safe: bool
    read_only: bool


def validate_reasoning_result_conformance(
    result: PathReasoningResult,
    policy: ReasoningPolicy,
) -> ConformanceReport:
    """Verify that a reasoning result stays outside canonical truth and mutation by default."""
    try:
        validate_truth_transition(TruthClass.DERIVED, TruthClass.DERIVED, policy)
        validate_graph_mutation(policy)
    except ValueError as exc:
        if "graph mutation" in str(exc):
            return ConformanceReport(result.result_ref, True, False)
        raise ReasoningConformanceError(str(exc)) from exc
    return ConformanceReport(result.result_ref, True, True)
