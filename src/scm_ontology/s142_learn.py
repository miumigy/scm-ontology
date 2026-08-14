from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class LearningStatus(str, Enum):
    PROPOSED = "proposed"
    ASSESSED = "assessed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


class LearningTargetType(str, Enum):
    KNOWLEDGE = "knowledge"
    ASSUMPTION = "assumption"
    POLICY = "policy"
    RULE = "rule"
    MODEL = "model"
    DECISION_CONTEXT = "decision_context"


@dataclass(frozen=True)
class LearningResult:
    ref: str
    subject_ref: str
    target_type: LearningTargetType
    conclusion: str
    status: LearningStatus = LearningStatus.PROPOSED
    evidence_refs: tuple[str, ...] = ()
    outcome_refs: tuple[str, ...] = ()
    performance_refs: tuple[str, ...] = ()
    diagnosis_refs: tuple[str, ...] = ()
    causal_assessment_refs: tuple[str, ...] = ()
    prior_target_ref: Optional[str] = None
    successor_target_ref: Optional[str] = None
    confidence_ref: Optional[str] = None
    scenario_ref: Optional[str] = None
    learned_at: Optional[str] = None
    effective_at: Optional[str] = None
    provenance_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.ref or not self.subject_ref or not self.conclusion:
            raise ValueError("ref, subject_ref, and conclusion are required")

    @property
    def is_measurement(self) -> bool:
        return False

    @property
    def is_decision(self) -> bool:
        return False

    @property
    def is_policy(self) -> bool:
        return self.target_type is LearningTargetType.POLICY

    @property
    def is_scenario_learning(self) -> bool:
        return self.scenario_ref is not None


def record_learning(
    *,
    ref: str,
    subject_ref: str,
    target_type: LearningTargetType,
    conclusion: str,
    status: LearningStatus = LearningStatus.PROPOSED,
    evidence_refs: tuple[str, ...] = (),
    outcome_refs: tuple[str, ...] = (),
    performance_refs: tuple[str, ...] = (),
    diagnosis_refs: tuple[str, ...] = (),
    causal_assessment_refs: tuple[str, ...] = (),
    prior_target_ref: Optional[str] = None,
    successor_target_ref: Optional[str] = None,
    confidence_ref: Optional[str] = None,
    scenario_ref: Optional[str] = None,
    learned_at: Optional[str] = None,
    effective_at: Optional[str] = None,
    provenance_refs: tuple[str, ...] = (),
) -> LearningResult:
    return LearningResult(
        ref=ref,
        subject_ref=subject_ref,
        target_type=target_type,
        conclusion=conclusion,
        status=status,
        evidence_refs=evidence_refs,
        outcome_refs=outcome_refs,
        performance_refs=performance_refs,
        diagnosis_refs=diagnosis_refs,
        causal_assessment_refs=causal_assessment_refs,
        prior_target_ref=prior_target_ref,
        successor_target_ref=successor_target_ref,
        confidence_ref=confidence_ref,
        scenario_ref=scenario_ref,
        learned_at=learned_at,
        effective_at=effective_at,
        provenance_refs=provenance_refs,
    )
