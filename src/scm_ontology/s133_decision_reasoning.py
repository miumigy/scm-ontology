from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class DecisionStage(str, Enum):
    EVALUATION = "evaluation"
    RECOMMENDATION = "recommendation"
    DECISION = "decision"


@dataclass(frozen=True)
class Alternative:
    ref: str
    label: str
    constraint_evaluation_refs: tuple[str, ...] = ()
    what_if_result_refs: tuple[str, ...] = ()
    causal_assessment_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.ref or not self.label:
            raise ValueError("ref and label are required")


@dataclass(frozen=True)
class DecisionEvaluation:
    ref: str
    alternative_refs: tuple[str, ...]
    objective_refs: tuple[str, ...] = ()
    constraint_refs: tuple[str, ...] = ()
    policy_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    epistemic_status: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.ref or not self.alternative_refs:
            raise ValueError("ref and at least one alternative are required")


@dataclass(frozen=True)
class Recommendation:
    ref: str
    selected_alternative_ref: str
    evaluation_ref: str
    rationale: Optional[str] = None
    uncertainty: Optional[str] = None

    @property
    def is_decision(self) -> bool:
        return False


@dataclass(frozen=True)
class Decision:
    ref: str
    selected_alternative_ref: str
    evaluation_ref: str
    authority_ref: str
    decided_at: str
    recommendation_ref: Optional[str] = None
    rationale: Optional[str] = None

    @property
    def is_recommendation(self) -> bool:
        return False


def create_recommendation(
    *,
    ref: str,
    selected_alternative_ref: str,
    evaluation_ref: str,
    rationale: Optional[str] = None,
    uncertainty: Optional[str] = None,
) -> Recommendation:
    return Recommendation(
        ref=ref,
        selected_alternative_ref=selected_alternative_ref,
        evaluation_ref=evaluation_ref,
        rationale=rationale,
        uncertainty=uncertainty,
    )


def create_decision(
    *,
    ref: str,
    selected_alternative_ref: str,
    evaluation_ref: str,
    authority_ref: str,
    decided_at: str,
    recommendation_ref: Optional[str] = None,
    rationale: Optional[str] = None,
) -> Decision:
    if not authority_ref:
        raise ValueError("a Decision requires an authority_ref")
    if not decided_at:
        raise ValueError("a Decision requires decided_at")
    return Decision(
        ref=ref,
        selected_alternative_ref=selected_alternative_ref,
        evaluation_ref=evaluation_ref,
        authority_ref=authority_ref,
        decided_at=decided_at,
        recommendation_ref=recommendation_ref,
        rationale=rationale,
    )
