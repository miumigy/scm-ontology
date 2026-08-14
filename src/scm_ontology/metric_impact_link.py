"""Canonical relationship between an impact and a metric."""
from __future__ import annotations

from dataclasses import dataclass

from .simulation import SimulationError


class MetricImpactLinkError(SimulationError):
    """Raised when a metric impact link violates its semantic contract."""


@dataclass(frozen=True)
class MetricImpactLink:
    """An immutable semantic relationship from an impact to a metric."""

    impact_id: str
    metric_id: str
    relationship: str


def link_metric_impact(
    impact_id: str,
    metric_id: str,
    relationship: str = "impacts",
) -> MetricImpactLink:
    """Create a validated impact-to-metric relationship."""
    if not impact_id:
        raise MetricImpactLinkError("impact_id is required")
    if not metric_id:
        raise MetricImpactLinkError("metric_id is required")
    if relationship != "impacts":
        raise MetricImpactLinkError("relationship must be impacts")

    return MetricImpactLink(
        impact_id=impact_id,
        metric_id=metric_id,
        relationship=relationship,
    )
