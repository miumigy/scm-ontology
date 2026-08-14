from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class EvaluationResult(str, Enum):
    SATISFIED = "satisfied"
    VIOLATED = "violated"
    UNKNOWN = "unknown"
    NOT_APPLICABLE = "not_applicable"


class SemanticKind(str, Enum):
    RULE = "rule"
    CONSTRAINT = "constraint"


@dataclass(frozen=True)
class ReasoningInput:
    subject_ref: str
    evidence_refs: tuple[str, ...] = ()
    epistemic_status: Optional[str] = None
    scenario_ref: Optional[str] = None
    effective_at: Optional[str] = None
    observed_at: Optional[str] = None


@dataclass(frozen=True)
class RuleOrConstraint:
    ref: str
    kind: SemanticKind
    expression: str
    effective_from: Optional[str] = None
    effective_to: Optional[str] = None


@dataclass(frozen=True)
class Evaluation:
    semantic_ref: str
    input_ref: str
    result: EvaluationResult
    evidence_refs: tuple[str, ...] = ()
    scenario_ref: Optional[str] = None
    explanation: Optional[str] = None
    severity: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.semantic_ref or not self.input_ref:
            raise ValueError("semantic_ref and input_ref are required")
        if self.result is EvaluationResult.VIOLATED and not self.evidence_refs:
            raise ValueError("a violated evaluation requires evidence_refs")

    @property
    def can_be_decision(self) -> bool:
        return False


def evaluate_known(value: bool, *, semantic_ref: str, input_ref: str,
                   evidence_refs: tuple[str, ...] = (),
                   scenario_ref: Optional[str] = None) -> Evaluation:
    """Create a semantic evaluation without crossing into Decision semantics."""
    result = EvaluationResult.SATISFIED if value else EvaluationResult.VIOLATED
    return Evaluation(
        semantic_ref=semantic_ref,
        input_ref=input_ref,
        result=result,
        evidence_refs=evidence_refs,
        scenario_ref=scenario_ref,
    )
