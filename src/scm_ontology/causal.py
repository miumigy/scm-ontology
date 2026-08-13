"""Deterministic causal propagation for simulation events."""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Mapping

from scm_ontology.simulation import Event


@dataclass(frozen=True)
class CausalRule:
    """A canonical event-to-event causal rule."""

    rule_id: str
    source_event_type: str
    target_event_type: str


@dataclass(frozen=True)
class EventProvenance:
    """Lineage metadata for a derived event."""

    caused_by_event_id: str | None = None
    rule_id: str | None = None
    causal_depth: int = 0


class CausalPropagationError(ValueError):
    """Raised when causal propagation would be ambiguous or cyclic."""


def derive_event(source: Event, rule: CausalRule, *, event_id: str) -> Event:
    """Derive one deterministic event while preserving causal provenance."""
    if source.event_type != rule.source_event_type:
        raise CausalPropagationError(
            f"rule {rule.rule_id} cannot consume event type {source.event_type}"
        )
    provenance = source.provenance or EventProvenance()
    if provenance.rule_id == rule.rule_id:
        raise CausalPropagationError(
            f"causal rule already applied in lineage: {rule.rule_id}"
        )
    next_provenance = EventProvenance(
        caused_by_event_id=source.event_id,
        rule_id=rule.rule_id,
        causal_depth=provenance.causal_depth + 1,
    )
    return replace(
        source,
        event_id=event_id,
        event_type=rule.target_event_type,
        provenance=next_provenance,
    )


def propagate_event(source: Event, rules: Mapping[str, CausalRule], *, event_id: str) -> Event | None:
    """Apply the matching causal rule deterministically, if exactly one exists."""
    matches = [rule for rule in rules.values() if rule.source_event_type == source.event_type]
    if len(matches) > 1:
        raise CausalPropagationError(
            f"ambiguous causal rules for event type {source.event_type}"
        )
    if not matches:
        return None
    return derive_event(source, matches[0], event_id=event_id)
