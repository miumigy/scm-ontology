"""Canonical relationship between an observation and its entity."""
from __future__ import annotations

from dataclasses import dataclass

from .simulation import SimulationError


class ObservationEntityLinkError(SimulationError):
    """Raised when an observation-entity link violates its contract."""


@dataclass(frozen=True)
class ObservationEntityLink:
    """An immutable relationship identifying what an observation is about."""

    observation_id: str
    entity_id: str
    relationship: str


def link_observation_entity(
    observation_id: str,
    entity_id: str,
    relationship: str = "observed_for",
) -> ObservationEntityLink:
    """Create a validated observation-to-entity relationship."""
    if not observation_id:
        raise ObservationEntityLinkError("observation_id is required")
    if not entity_id:
        raise ObservationEntityLinkError("entity_id is required")
    if relationship != "observed_for":
        raise ObservationEntityLinkError("relationship must be observed_for")

    return ObservationEntityLink(
        observation_id=observation_id,
        entity_id=entity_id,
        relationship=relationship,
    )
