from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class EvidenceRole(str, Enum):
    SUPPORTING = "supporting"
    CONTRADICTING = "contradicting"
    CONTEXTUAL = "contextual"
    DERIVED = "derived"
    BASELINE = "baseline"
    SCENARIO_INPUT = "scenario_input"


@dataclass(frozen=True)
class EvidenceReference:
    ref: str
    role: EvidenceRole
    epistemic_status: Optional[str] = None
    authority_ref: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.ref:
            raise ValueError("ref is required")


@dataclass(frozen=True)
class ReasoningStep:
    ref: str
    kind: str
    input_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    output_refs: tuple[str, ...] = ()
    epistemic_status: Optional[str] = None
    semantic_version: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.ref or not self.kind:
            raise ValueError("ref and kind are required")


@dataclass(frozen=True)
class Explanation:
    ref: str
    subject_ref: str
    step_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    scenario_ref: Optional[str] = None

    @property
    def is_decision(self) -> bool:
        return False

    @property
    def invents_evidence(self) -> bool:
        return False


def build_explanation(
    *,
    ref: str,
    subject_ref: str,
    step_refs: tuple[str, ...] = (),
    evidence_refs: tuple[str, ...] = (),
    scenario_ref: Optional[str] = None,
) -> Explanation:
    if not ref or not subject_ref:
        raise ValueError("ref and subject_ref are required")
    return Explanation(
        ref=ref,
        subject_ref=subject_ref,
        step_refs=step_refs,
        evidence_refs=evidence_refs,
        scenario_ref=scenario_ref,
    )
