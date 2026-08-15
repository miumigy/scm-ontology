from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Optional

from .provenance import Provenance
from .temporal_state_event import TemporalAssertion, TemporalKind


class EpistemicKind(StrEnum):
    FACT = "fact"
    OBSERVATION = "observation"
    MEASUREMENT = "measurement"
    ESTIMATE = "estimate"
    PREDICTION = "prediction"
    INFERENCE = "inference"
    ASSUMPTION = "assumption"
    HYPOTHESIS = "hypothesis"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class SemanticContext:
    """Cross-cutting context for one canonical semantic assertion.

    The context binds temporal, provenance, and epistemic dimensions without
    collapsing them into one status. It is intentionally storage-neutral.
    """

    assertion_ref: str
    subject_ref: str
    epistemic_kind: EpistemicKind
    temporal_assertions: tuple[TemporalAssertion, ...] = ()
    provenance: Optional[Provenance] = None
    confidence: Optional[float] = None
    source_ref: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.assertion_ref or not self.subject_ref:
            raise ValueError("assertion_ref and subject_ref are required")
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if self.epistemic_kind is EpistemicKind.FACT and self.confidence is not None:
            raise ValueError("fact assertions do not use confidence as an epistemic status")
        if self.epistemic_kind is EpistemicKind.UNKNOWN and self.temporal_assertions:
            if any(item.kind is TemporalKind.ACTUAL for item in self.temporal_assertions):
                raise ValueError("unknown assertions cannot claim an actual temporal assertion")

    @property
    def has_provenance(self) -> bool:
        return self.provenance is not None

    def temporal_kinds(self) -> frozenset[TemporalKind]:
        return frozenset(item.kind for item in self.temporal_assertions)
