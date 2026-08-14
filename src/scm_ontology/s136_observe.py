from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ObservationEpistemicStatus(str, Enum):
    OBSERVED = "observed"
    ESTIMATED = "estimated"
    PREDICTED = "predicted"
    INFERRED = "inferred"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Observation:
    ref: str
    subject_ref: str
    observed_at: str
    value: object
    source_ref: Optional[str] = None
    method_ref: Optional[str] = None
    unit_ref: Optional[str] = None
    uncertainty: Optional[str] = None
    provenance_refs: tuple[str, ...] = ()
    epistemic_status: ObservationEpistemicStatus = ObservationEpistemicStatus.OBSERVED

    def __post_init__(self) -> None:
        if not self.ref or not self.subject_ref or not self.observed_at:
            raise ValueError("ref, subject_ref, and observed_at are required")

    @property
    def is_event(self) -> bool:
        return False

    @property
    def is_state(self) -> bool:
        return False

    @property
    def is_inference(self) -> bool:
        return self.epistemic_status is ObservationEpistemicStatus.INFERRED


def record_observation(
    *,
    ref: str,
    subject_ref: str,
    observed_at: str,
    value: object,
    source_ref: Optional[str] = None,
    method_ref: Optional[str] = None,
    unit_ref: Optional[str] = None,
    uncertainty: Optional[str] = None,
    provenance_refs: tuple[str, ...] = (),
    epistemic_status: ObservationEpistemicStatus = ObservationEpistemicStatus.OBSERVED,
) -> Observation:
    return Observation(
        ref=ref,
        subject_ref=subject_ref,
        observed_at=observed_at,
        value=value,
        source_ref=source_ref,
        method_ref=method_ref,
        unit_ref=unit_ref,
        uncertainty=uncertainty,
        provenance_refs=provenance_refs,
        epistemic_status=epistemic_status,
    )
