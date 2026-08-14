"""Canonical target semantics for causal impacts."""
from __future__ import annotations

from dataclasses import dataclass

from .causal_impact import ImpactResult
from .simulation import SimulationError


class ImpactTargetError(SimulationError):
    """Raised when an impact target violates its semantic contract."""


@dataclass(frozen=True)
class ImpactTarget:
    """Stable semantic reference for the target of an impact."""

    target_id: str
    target_type: str
    impact_type: str
    semantic_ref: str


def bind_impact_target(
    impact: ImpactResult,
    target_id: str,
    target_type: str,
    semantic_ref: str,
) -> ImpactTarget:
    """Bind an existing impact to a canonical semantic target without side effects."""
    if not target_id:
        raise ImpactTargetError("target_id is required")
    if not target_type:
        raise ImpactTargetError("target_type is required")
    if not semantic_ref:
        raise ImpactTargetError("semantic_ref is required")

    return ImpactTarget(
        target_id=target_id,
        target_type=target_type,
        impact_type=impact.impact_type,
        semantic_ref=semantic_ref,
    )
