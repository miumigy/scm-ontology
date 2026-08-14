from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class CausalAssessmentResult(str, Enum):
    SUPPORTED = "supported"
    UNSUPPORTED = "unsupported"
    UNCERTAIN = "uncertain"
    CONFOUNDED = "confounded"
    NOT_ASSESSABLE = "not_assessable"


@dataclass(frozen=True)
class CausalClaim:
    ref: str
    cause_ref: str
    effect_ref: str
    relationship_ref: str
    scenario_ref: Optional[str] = None
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.ref or not self.cause_ref or not self.effect_ref:
            raise ValueError("ref, cause_ref, and effect_ref are required")
        if self.cause_ref == self.effect_ref:
            raise ValueError("cause_ref and effect_ref must differ")


@dataclass(frozen=True)
class CausalAssessment:
    claim_ref: str
    result: CausalAssessmentResult
    evidence_refs: tuple[str, ...] = ()
    confounder_refs: tuple[str, ...] = ()
    attribution_ref: Optional[str] = None
    scenario_ref: Optional[str] = None
    explanation: Optional[str] = None

    @property
    def is_decision(self) -> bool:
        return False

    @property
    def is_counterfactual(self) -> bool:
        return self.scenario_ref is not None


def assess_claim(
    claim: CausalClaim,
    *,
    result: CausalAssessmentResult,
    evidence_refs: tuple[str, ...] = (),
    confounder_refs: tuple[str, ...] = (),
    attribution_ref: Optional[str] = None,
) -> CausalAssessment:
    if result is CausalAssessmentResult.SUPPORTED and not evidence_refs:
        raise ValueError("supported causal claims require evidence_refs")
    if attribution_ref and result is CausalAssessmentResult.SUPPORTED and not evidence_refs:
        raise ValueError("attribution cannot substitute for causal evidence")
    return CausalAssessment(
        claim_ref=claim.ref,
        result=result,
        evidence_refs=evidence_refs,
        confounder_refs=confounder_refs,
        attribution_ref=attribution_ref,
        scenario_ref=claim.scenario_ref,
    )
