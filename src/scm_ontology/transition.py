"""Explicit state transition rules for canonical simulation properties."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from scm_ontology.simulation import Event, SimulationError, State


@dataclass(frozen=True)
class StateTransitionRule:
    """Maps one event type to one explicit canonical state-property transition."""

    rule_id: str
    event_type: str
    entity_type: str
    property_name: str
    attribute_name: str


def apply_transition_rule(
    state: State, event: Event, rule: StateTransitionRule
) -> tuple[State, Mapping[str, Mapping[str, Any]]]:
    """Apply a validated numeric increment without mutating the input state."""
    if event.event_type != rule.event_type:
        raise SimulationError(
            f"rule {rule.rule_id} cannot consume event type {event.event_type}"
        )
    if event.entity_id not in state.entities:
        raise SimulationError(f"Unknown entity: {event.entity_id}")

    entity = dict(state.entities[event.entity_id])
    if entity.get("entityType") != rule.entity_type:
        raise SimulationError(
            f"{rule.event_type} requires {rule.entity_type} entity"
        )

    magnitude = event.attributes.get(rule.attribute_name)
    before = entity.get(rule.property_name)
    if not isinstance(magnitude, int) or magnitude < 0:
        raise SimulationError(
            f"{rule.event_type} {rule.attribute_name} must be a non-negative integer"
        )
    if not isinstance(before, int) or before < 0:
        raise SimulationError(
            f"{rule.property_name} must be a non-negative integer"
        )

    after = before + magnitude
    next_entities = dict(state.entities)
    next_entity = dict(entity)
    next_entity[rule.property_name] = after
    next_entities[event.entity_id] = next_entity
    next_state = State(
        f"{state.state_id}@{event.occurred_at}:{event.event_id}",
        event.occurred_at,
        next_entities,
        dict(state.relationship_states),
    )
    return next_state, {rule.property_name: {"before": before, "after": after}}


SUPPLIER_DELAY_LEAD_TIME_RULE = StateTransitionRule(
    rule_id="TRANS-SUPPLIER-DELAY-LEAD-TIME",
    event_type="SUPPLIER_DELAY",
    entity_type="Party",
    property_name="leadTimeDays",
    attribute_name="magnitudeDays",
)
