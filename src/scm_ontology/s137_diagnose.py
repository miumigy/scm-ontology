from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class DiagnosisEpistemicStatus(str, Enum):
    OBSERVED = "observed"
    ESTIMATED = "estimated"
    INFERRED = "inferred"
    HYPOTHESIZED = "hypothesized"
    UNKNOWN = "unknown"


class FindingType(str, Enum):
    DEVIATION = "deviation"
    EXCEPTION = "exception"
    CONDITION = "condition"
    CANDIDATE_CAUSE = "candidate_cause"


@dataclass(frozen=True)
class DiagnosticFinding:
    ref: str
    finding_type: FindingType
    subject_ref: str
    description: str
    evidence_refs: tuple[str, ...] = ()
    causal_assessment_refs: tuple[str, ...] = ()
    epistemic_status: DiagnosisEpistemicStatus = DiagnosisEpistemicStatus.UNKNOWN

    def __post_init__(self) -> None:
        if not self.ref or not self.subject_ref or not self.description:
            raise ValueError("ref, subject_ref, and description are required")


@dataclass(frozen=True)
class Diagnosis:
    ref: str
    subject_ref: str
    finding_refs: tuple[str, ...]
    period_start: Optional[str] = None
    period_end: Optional[str] = None
    scenario_ref: Optional[str] = None
    evidence_refs: tuple[str, ...] = ()
    causal_assessment_refs: tuple[str, ...] = ()
    hypothesis_refs: tuple[str, ...] = ()
    epistemic_status: DiagnosisEpistemicStatus = DiagnosisEpistemicStatus.UNKNOWN

    def __post_init__(self) -> None:
        if not self.ref or not self.subject_ref or not self.finding_refs:
            raise ValueError("ref, subject_ref, and finding_refs are required")

    @property
    def is_scenario_diagnosis(self) -> bool:
        return self.scenario_ref is not None

    @property
    def is_decision(self) -> bool:
        return False

    @property
    def is_action(self) -> bool:
        return False


def build_diagnosis(
    *,
    ref: str,
    subject_ref: str,
    finding_refs: tuple[str, ...],
    period_start: Optional[str] = None,
    period_end: Optional[str] = None,
    scenario_ref: Optional[str] = None,
    evidence_refs: tuple[str, ...] = (),
    causal_assessment_refs: tuple[str, ...] = (),
    hypothesis_refs: tuple[str, ...] = (),
    epistemic_status: DiagnosisEpistemicStatus = DiagnosisEpistemicStatus.UNKNOWN,
) -> Diagnosis:
    return Diagnosis(
        ref=ref,
        subject_ref=subject_ref,
        finding_refs=finding_refs,
        period_start=period_start,
        period_end=period_end,
        scenario_ref=scenario_ref,
        evidence_refs=evidence_refs,
        causal_assessment_refs=causal_assessment_refs,
        hypothesis_refs=hypothesis_refs,
        epistemic_status=epistemic_status,
    )
