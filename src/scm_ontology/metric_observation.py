"""Canonical observations of SCM metrics."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .simulation import SimulationError


class MetricObservationError(SimulationError):
    """Raised when a metric observation violates its semantic contract."""


@dataclass(frozen=True)
class MetricObservation:
    """An immutable observation of a metric, independent of calculation logic."""

    metric_id: str
    value: float
    observed_at: datetime
    entity_id: str
    source_ref: str


def observe_metric(
    metric_id: str,
    value: float,
    observed_at: datetime,
    entity_id: str,
    source_ref: str,
) -> MetricObservation:
    """Create a validated metric observation without modifying metric semantics."""
    if not metric_id:
        raise MetricObservationError("metric_id is required")
    if not isinstance(observed_at, datetime) or observed_at.tzinfo is None:
        raise MetricObservationError("observed_at must be timezone-aware")
    if not entity_id:
        raise MetricObservationError("entity_id is required")
    if not source_ref:
        raise MetricObservationError("source_ref is required")

    return MetricObservation(
        metric_id=metric_id,
        value=float(value),
        observed_at=observed_at,
        entity_id=entity_id,
        source_ref=source_ref,
    )
