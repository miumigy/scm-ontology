# SCM Simulation Semantic Contract v0.1

Status: S1 implementation contract  
Date: 2026-08-14

## 1. Purpose

This document defines the minimum semantic contract between the SCM Ontology and the deterministic simulation kernel introduced in S1.

The contract is intentionally smaller than the future simulation architecture. It establishes how canonical SCM state is projected into a simulation state, how events produce transitions, and how a run remains reproducible and machine-readable.

The simulation kernel is a consumer of canonical semantics. It does not define, extend, or mutate the SCM Ontology.

## 2. Core contract

The minimum execution loop is:

```text
Scenario
   |
   v
Initial State
   |
   +---- Event
   |       |
   |       v
   |   Transition
   |       |
   |       v
   +--> New State
           |
           v
     Simulation Result
```

A transition is explicit:

```text
(previous State, Event) -> (new State, Transition record)
```

S1 does not yet require decisions, constraints, KPI calculation, causal propagation, or graph persistence in the runtime.

## 3. Canonical state projection

Simulation State is a **projection of canonical SCM entity state**, not a new ontology.

Canonical entity identity remains the canonical `id`:

```json
{
  "id": "SUP-A",
  "entityType": "Party",
  "partyType": "SUPPLIER",
  "leadTimeDays": 5
}
```

The simulation may maintain mutable operational attributes such as `leadTimeDays`, `quantity`, `available`, and `inTransit` inside a time-indexed State snapshot.

These attributes do not become independent canonical entities merely because the simulator uses them.

### Invariant

Simulation state must never introduce a second identity system for canonical entities such as Product, Site, Material, Party, ProductLocation, Demand, or InventoryPosition.

## 4. State

A State contains:

- stable `state_id`
- simulation/effective time
- canonical entity-keyed state data

Conceptually:

```text
State {
  state_id
  effective_at
  entities: {
    canonical_entity_id -> canonical state projection
  }
}
```

State transitions are non-destructive. Applying an Event produces a new State; the input State remains unchanged.

## 5. Event

An Event contains:

- stable event id
- event type
- occurrence time
- affected canonical entity id
- event attributes

Example:

```json
{
  "id": "E-001",
  "eventType": "SUPPLIER_DELAY",
  "occurredAt": 7,
  "entityId": "SUP-A",
  "attributes": {
    "magnitudeDays": 7
  }
}
```

An Event describes an occurrence. It does not directly mutate State.

## 6. Transition

Every successful Event application produces an inspectable Transition.

Minimum fields:

```text
transition_id
 event_id
 event_type
 from_state_id
 to_state_id
 entity_id
 changes
```

`changes` records before/after values.

Example:

```json
{
  "leadTimeDays": {
    "before": 5,
    "after": 12
  }
}
```

This makes the simulation explainable without inspecting implementation internals.

## 7. Determinism

For S1:

```text
same Scenario
+ same baseline State
+ same event set
+ same seed
= same SimulationRun
```

Run identifiers are derived from canonicalized run inputs rather than wall-clock time or process-local randomness.

Events are ordered deterministically by:

```text
occurred_at
then event_id
```

The seed is persisted even though S1 does not yet use stochastic sampling. This establishes the contract required by later stochastic wrappers.

## 8. Example: Supplier delay

Baseline:

```text
SUP-A
leadTimeDays = 5
```

Scenario Event:

```text
SUPPLIER_DELAY
magnitudeDays = 7
```

Transition:

```text
5 -> 12
```

Resulting State:

```text
SUP-A
leadTimeDays = 12
```

No unrelated entity is changed by this event.

## 9. Existing Demand-Supply semantics

The S1 simulation state can represent the existing M6 semantic calculation without redefining it:

```text
Demand = 100
Available = 60
Inbound = 20
Relevant Supply = 80
Gap = 20
```

`Demand.quantity`, `InventoryPosition.available`, and `InventoryPosition.inTransit` are projections of existing canonical entities.

A supplier-delay event that only changes supplier lead time must not alter this gap unless a later transition explicitly models the effect on supply timing.

This preserves semantic separation between:

```text
Supplier lead-time state

and

Demand-supply availability state
```

## 10. SimulationRun

A SimulationRun is a first-class machine-readable result containing at least:

- simulation run id
- scenario id
- seed
- initial state
- ordered events
- transitions
- final state

Future versions may add engine version, ontology version, KPI outcomes, risks, causal impacts, decisions, and state deltas without changing the S1 meaning of the core fields.

## 11. Graph compatibility

S1 does not require Neo4j. However, the result must contain enough stable identifiers and explicit transition records for a future adapter to represent:

```text
State -> Event -> Transition -> State
```

in SCM Graph form.

The kernel must not write directly to a graph database.

## 12. Semantic boundary

The following are explicitly outside S1:

- automatic causal propagation
- KPI/risk engine
- optimization
- Monte Carlo
- LLM/AI Agent
- Neo4j runtime dependency
- browser UI
- legacy `scsim` dependency
- new canonical ontology entities created solely for simulation

These are later architectural layers.

## 13. S1 acceptance criteria

S1 is complete when:

1. A canonical entity-keyed State can be constructed.
2. An Event can be applied without mutating the input State.
3. A valid Event produces a deterministic Transition and new State.
4. Invalid Event/entity combinations are rejected.
5. Event ordering is deterministic.
6. Same Scenario + Seed produces the same run.
7. Existing Demand-Supply semantics remain unchanged by unrelated events.
8. SimulationRun is machine-readable and graph-adapter friendly.
9. The kernel has no Neo4j or legacy `scsim` dependency.
10. CI validates the semantic and runtime tests.
