from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class MeasurementStatus(str, Enum):
    OBSERVED = "observed"
    ESTIMATED = "estimated"
    MISSING = "missing"
    STALE = "stale"
    RESTATED = "restated"


@dataclass(frozen=True)
class MeasurementRecord:
    ref: str
    subject_ref: str
    value: Optional[float]
    unit_ref: Optional[str] = None
    observation_time: Optional[str] = None
    transaction_time: Optional[str] = None
    method_ref: Optional[str] = None
    source_ref: Optional[str] = None
    uncertainty_ref: Optional[str] = None
    status: MeasurementStatus = MeasurementStatus.OBSERVED
    provenance_refs: tuple[str, ...] = ()
    predecessor_ref: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.ref or not self.subject_ref:
            raise ValueError("ref and subject_ref are required")
        if self.status in {MeasurementStatus.MISSING, MeasurementStatus.STALE} and self.value is not None:
            raise ValueError("missing or stale measurements must not carry a current value")

    @property
    def is_actual(self) -> bool:
        return self.status is MeasurementStatus.OBSERVED

    @property
    def is_metric(self) -> bool:
        return False

    @property
    def is_performance_assessment(self) -> bool:
        return False


@dataclass(frozen=True)
class PerformanceAssessment:
    ref: str
    subject_ref: str
    metric_value_refs: tuple[str, ...]
    comparison_basis_refs: tuple[str, ...] = ()
    variance_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    scenario_ref: Optional[str] = None
    provenance_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.ref or not self.subject_ref or not self.metric_value_refs:
            raise ValueError("ref, subject_ref, and metric_value_refs are required")

    @property
    def is_decision(self) -> bool:
        return False


def record_measurement(
    *,
    ref: str,
    subject_ref: str,
    value: Optional[float],
    unit_ref: Optional[str] = None,
    observation_time: Optional[str] = None,
    transaction_time: Optional[str] = None,
    method_ref: Optional[str] = None,
    source_ref: Optional[str] = None,
    uncertainty_ref: Optional[str] = None,
    status: MeasurementStatus = MeasurementStatus.OBSERVED,
    provenance_refs: tuple[str, ...] = (),
    predecessor_ref: Optional[str] = None,
) -> MeasurementRecord:
    return MeasurementRecord(
        ref=ref,
        subject_ref=subject_ref,
        value=value,
        unit_ref=unit_ref,
        observation_time=observation_time,
        transaction_time=transaction_time,
        method_ref=method_ref,
        source_ref=source_ref,
        uncertainty_ref=uncertainty_ref,
        status=status,
        provenance_refs=provenance_refs,
        predecessor_ref=predecessor_ref,
    )
