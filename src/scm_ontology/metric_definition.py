"""Canonical semantic definitions for SCM metrics."""
from __future__ import annotations

from dataclasses import dataclass

from .simulation import SimulationError


class MetricDefinitionError(SimulationError):
    """Raised when a metric definition violates its semantic contract."""


@dataclass(frozen=True)
class MetricDefinition:
    """Stable semantic definition of a metric, independent of calculation logic."""

    metric_id: str
    metric_type: str
    semantic_ref: str
    unit: str
    direction: str


def define_metric(
    metric_id: str,
    metric_type: str,
    semantic_ref: str,
    unit: str,
    direction: str,
) -> MetricDefinition:
    """Create a validated, immutable metric definition."""
    if not metric_id:
        raise MetricDefinitionError("metric_id is required")
    if not metric_type:
        raise MetricDefinitionError("metric_type is required")
    if not semantic_ref:
        raise MetricDefinitionError("semantic_ref is required")
    if not unit:
        raise MetricDefinitionError("unit is required")
    if direction not in {"higher_is_better", "lower_is_better"}:
        raise MetricDefinitionError(
            "direction must be higher_is_better or lower_is_better"
        )

    return MetricDefinition(
        metric_id=metric_id,
        metric_type=metric_type,
        semantic_ref=semantic_ref,
        unit=unit,
        direction=direction,
    )
