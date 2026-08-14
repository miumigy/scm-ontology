"""Canonical projection of a causal chain into an auditable impact result."""
from __future__ import annotations

from dataclasses import dataclass

from .causal_chain import CausalChain
from .simulation import SimulationError


class CausalImpactError(SimulationError):
    """Raised when a causal impact violates its semantic contract."""


@dataclass(frozen=True)
class ImpactResult:
    """Deterministic, side-effect-free projection of a causal chain."""

    source_event_id: str
    terminal_event_id: str
    causal_depth: int
    affected_entity_id: str
    impact_type: str
    magnitude: float
    unit: str
    causal_event_ids: tuple[str, ...]


def project_impact(
    chain: CausalChain,
    affected_entity_id: str,
    impact_type: str,
    magnitude: float,
    unit: str,
) -> ImpactResult:
    """Project a completed causal chain into a canonical impact result."""
    if not affected_entity_id:
        raise CausalImpactError("affected_entity_id is required")
    if not impact_type:
        raise CausalImpactError("impact_type is required")
    if not unit:
        raise CausalImpactError("unit is required")

    return ImpactResult(
        source_event_id=chain.events[0].event_id,
        terminal_event_id=chain.terminal_event.event_id,
        causal_depth=chain.depth,
        affected_entity_id=affected_entity_id,
        impact_type=impact_type,
        magnitude=magnitude,
        unit=unit,
        causal_event_ids=tuple(event.event_id for event in chain.events),
    )
