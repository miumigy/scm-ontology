# S7 — Causal Event → State Transition Contract

## Purpose

S7 connects the existing causal-event model with the S5/S6 canonical state-transition kernel without moving state mutation into causal propagation.

## Contract

```text
Source Event
    │
    │ CausalRule / CAUSES
    ▼
Derived Event
    │
    │ SimulationKernel
    ▼
Transition
    │
    ▼
New State
```

Causal propagation has the semantic signature `Event → Event`. State transition has the semantic signature `Event → State`. The S7 bridge composes these contracts but keeps their responsibilities separate.

## Auditability

Each derived event retains causal provenance including `causedByEventId` and `ruleId`. The bridge result retains the source event, derived event, transition, and resulting state so a simulation step can be audited without reconstructing hidden mutable state.

## Invariants

1. The same source event, causal rule, derived-event identity, and initial state produce the same result.
2. Causal derivation does not mutate the input state.
3. Only the simulation transition kernel changes State.
4. A derived event that has no valid transition is rejected explicitly.
5. Causal provenance remains attached to the derived event.
6. S7 does not define new SCM state semantics such as MATERIAL_SHORTAGE; those belong to a later transition-model milestone.

## Scope Boundary

S7 does not yet implement recursive causal propagation, KPI propagation, risk propagation, stochastic simulation, optimization, Neo4j runtime execution, or AI reasoning. It establishes the semantic bridge required for those later capabilities.
