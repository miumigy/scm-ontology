# SCM Simulation Semantic Contract v0.1

> Historical S1 implementation contract. Archived after M8 completion.

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

Canonical entity identity remains the canonical `id`.

### Invariant

Simulation state must never introduce a second identity system for canonical entities such as Product, Site, Material, Party, ProductLocation, Demand, or InventoryPosition.

## 4. State

A State contains stable `state_id`, simulation/effective time, and canonical entity-keyed state data. State transitions are non-destructive.

## 5. Event

An Event contains stable event id, event type, occurrence time, affected canonical entity id, and event attributes. An Event describes an occurrence; it does not directly mutate State.

## 6. Transition

Every successful Event application produces an inspectable Transition containing the event, source/target states, affected entity, and before/after changes.

## 7. Determinism

```text
same Scenario + same baseline State + same event set + same seed = same SimulationRun
```

Events are ordered deterministically by `occurred_at`, then `event_id`.

## 8. Demand-Supply semantics

The simulation state can represent existing M6 semantic calculations without redefining them. Unrelated events must not silently change demand-supply availability semantics.

## 9. SimulationRun

A SimulationRun contains at least run id, scenario id, seed, initial state, ordered events, transitions, and final state.

## 10. Graph compatibility

The result must contain stable identifiers and explicit transition records for a future graph adapter. The kernel must not write directly to a graph database.

## 11. Semantic boundary

Automatic causal propagation, KPI/risk engine, optimization, Monte Carlo, LLM/AI Agent, Neo4j runtime dependency, browser UI, legacy `scsim` dependency, and new canonical ontology entities created solely for simulation are outside S1.

## 12. S1 acceptance criteria

S1 is complete when canonical state can be constructed, events are applied immutably and deterministically, invalid combinations are rejected, runs are reproducible and machine-readable, and CI validates the semantic and runtime tests.
