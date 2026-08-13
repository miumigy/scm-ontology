"""Deterministic SCM simulation kernel and state projections."""
from __future__ import annotations
from dataclasses import dataclass, field
from hashlib import sha256
import copy, json
from typing import Any, Mapping

class SimulationError(ValueError):
    """Invalid simulation input or transition."""

@dataclass(frozen=True)
class EventProvenance:
    caused_by_event_id: str | None = None
    rule_id: str | None = None
    causal_depth: int = 0

@dataclass(frozen=True)
class State:
    state_id: str
    effective_at: int
    entities: Mapping[str, Mapping[str, Any]]
    relationship_states: Mapping[str, Mapping[str, Any]] = field(default_factory=dict)
    def snapshot(self) -> dict[str, Any]:
        return copy.deepcopy({"id": self.state_id, "effectiveAt": self.effective_at,
            "entities": dict(self.entities), "relationshipStates": dict(self.relationship_states)})

@dataclass(frozen=True)
class Event:
    event_id: str
    event_type: str
    occurred_at: int
    entity_id: str
    attributes: Mapping[str, Any] = field(default_factory=dict)
    provenance: EventProvenance | None = None

@dataclass(frozen=True)
class Transition:
    transition_id: str
    event_id: str
    event_type: str
    from_state_id: str
    to_state_id: str
    entity_id: str
    changes: Mapping[str, Mapping[str, Any]]

@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    baseline_state: State
    events: tuple[Event, ...] = ()
    seed: int = 0

@dataclass(frozen=True)
class SimulationRun:
    simulation_run_id: str
    scenario_id: str
    seed: int
    initial_state: State
    events: tuple[Event, ...]
    transitions: tuple[Transition, ...]
    final_state: State
    def to_dict(self) -> dict[str, Any]:
        return {"simulationRunId": self.simulation_run_id, "scenarioId": self.scenario_id, "seed": self.seed,
            "initialState": self.initial_state.snapshot(), "events": [_event_dict(e) for e in self.events],
            "transitions": [{"id": t.transition_id, "eventId": t.event_id, "eventType": t.event_type,
                "fromStateId": t.from_state_id, "toStateId": t.to_state_id, "entityId": t.entity_id,
                "changes": copy.deepcopy(dict(t.changes))} for t in self.transitions], "finalState": self.final_state.snapshot()}
    def canonical_payload(self) -> dict[str, Any]:
        return {"simulationRun": self.to_dict(),
            "events": [{"id": e.event_id, "eventType": e.event_type, "occurredAt": e.occurred_at,
                "entityId": e.entity_id} for e in self.events],
            "transitions": [{"id": t.transition_id, "eventId": t.event_id, "fromStateId": t.from_state_id,
                "toStateId": t.to_state_id, "entityId": t.entity_id} for t in self.transitions]}

class SimulationKernel:
    """Deterministic event -> transition -> state runtime for S1/S3."""
    def apply_event(self, state: State, event: Event) -> tuple[State, Transition]:
        if event.entity_id not in state.entities: raise SimulationError(f"Unknown entity: {event.entity_id}")
        if event.occurred_at < state.effective_at: raise SimulationError("Event time cannot precede state effective time")
        entity = copy.deepcopy(dict(state.entities[event.entity_id])); changes: dict[str, dict[str, Any]] = {}
        if event.event_type == "SUPPLIER_DELAY":
            if entity.get("entityType") != "Party" or entity.get("partyType") != "SUPPLIER": raise SimulationError("SUPPLIER_DELAY requires a supplier Party entity")
            magnitude = event.attributes.get("magnitudeDays")
            if not isinstance(magnitude, int) or magnitude < 0: raise SimulationError("SUPPLIER_DELAY magnitudeDays must be a non-negative integer")
            before = entity.get("leadTimeDays")
            if not isinstance(before, int) or before < 0: raise SimulationError("Supplier leadTimeDays must be a non-negative integer")
            after = before + magnitude; entity["leadTimeDays"] = after; changes["leadTimeDays"] = {"before": before, "after": after}
        else: raise SimulationError(f"Unsupported event type: {event.event_type}")
        next_entities = copy.deepcopy(dict(state.entities)); next_entities[event.entity_id] = entity
        next_state_id = f"{state.state_id}@{event.occurred_at}:{event.event_id}"
        next_state = State(next_state_id, event.occurred_at, next_entities, copy.deepcopy(dict(state.relationship_states)))
        transition_id = _stable_id({"event": event.event_id, "from": state.state_id, "to": next_state_id})
        return next_state, Transition(transition_id, event.event_id, event.event_type, state.state_id, next_state_id, event.entity_id, changes)

    def run(self, scenario: Scenario) -> SimulationRun:
        ordered_events = tuple(sorted(scenario.events, key=lambda e: (e.occurred_at, e.event_id)))
        state = scenario.baseline_state; transitions: list[Transition] = []
        for event in ordered_events: state, transition = self.apply_event(state, event); transitions.append(transition)
        run_id = _stable_id({"scenario": scenario.scenario_id, "seed": scenario.seed,
            "initialState": scenario.baseline_state.snapshot(), "events": [_event_dict(e) for e in ordered_events]})
        return SimulationRun(run_id, scenario.scenario_id, scenario.seed, scenario.baseline_state, ordered_events, tuple(transitions), state)

def _event_dict(event: Event) -> dict[str, Any]:
    data = {"id": event.event_id, "eventType": event.event_type, "occurredAt": event.occurred_at,
        "entityId": event.entity_id, "attributes": dict(event.attributes)}
    if event.provenance is not None: data["provenance"] = {"causedByEventId": event.provenance.caused_by_event_id,
        "ruleId": event.provenance.rule_id, "causalDepth": event.provenance.causal_depth}
    return data

def _stable_id(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return sha256(payload.encode()).hexdigest()[:16]
