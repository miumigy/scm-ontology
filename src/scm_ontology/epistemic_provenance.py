from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Optional


class EpistemicStatus(StrEnum):
    FACT = "fact"
    OBSERVATION = "observation"
    MEASUREMENT = "measurement"
    ESTIMATE = "estimate"
    PREDICTION = "prediction"
    INFERENCE = "inference"
    ASSUMPTION = "assumption"
    HYPOTHESIS = "hypothesis"
    UNKNOWN = "unknown"


class EvidenceRole(StrEnum):
    SUPPORTING = "supporting"
    CONTRADICTING = "contradicting"
    CONTEXT = "context"


@dataclass(frozen=True)
class Evidence:
    ref: str
    source_ref: str
    role: EvidenceRole = EvidenceRole.SUPPORTING
    observed_at: Optional[str] = None
    authority_ref: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.ref or not self.source_ref:
            raise ValueError("ref and source_ref are required")


@dataclass(frozen=True)
class EpistemicAssertion:
    ref: str
    subject_ref: str
    status: EpistemicStatus
    confidence: Optional[float] = None
    evidence_refs: tuple[str, ...] = ()
    provenance_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.ref or not self.subject_ref:
            raise ValueError("ref and subject_ref are required")
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if self.status is EpistemicStatus.UNKNOWN and self.confidence is not None:
            raise ValueError("unknown assertions must not claim confidence")

    @property
    def is_fact(self) -> bool:
        return self.status is EpistemicStatus.FACT

    @property
    def is_inference(self) -> bool:
        return self.status is EpistemicStatus.INFERENCE


@dataclass(frozen=True)
class ProvenanceAssertion:
    ref: str
    subject_ref: str
    source_refs: tuple[str, ...]
    derivation_rule_ref: Optional[str] = None
    transformation_ref: Optional[str] = None
    generated_at: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.ref or not self.subject_ref:
            raise ValueError("ref and subject_ref are required")
        if not self.source_refs:
            raise ValueError("source_refs must not be empty")


@dataclass(frozen=True)
class EvidenceAssessment:
    evidence_ref: str
    supports_assertion_ref: str
    strength: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.strength <= 1.0:
            raise ValueError("strength must be between 0 and 1")
