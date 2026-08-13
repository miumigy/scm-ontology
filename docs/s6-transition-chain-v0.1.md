# S6 — State Transition Chain v0.1

Status: Implementation contract
Date: 2026-08-14

## Purpose

S6 makes the deterministic simulation chain an explicit semantic contract. A `Scenario` supplies an ordered set of canonical `Event` objects. The kernel applies them one at a time, producing a new immutable `State` and an auditable `Transition` for each event.

```text
State₀ --Event₁--> State₁ --Event₂--> State₂ ... --Eventₙ--> Stateₙ
```

The simulation runtime remains a consumer of the SCM Ontology. S6 does not introduce simulator-specific entity identities or redefine canonical semantics.

## Invariants

1. Events are processed deterministically by `(occurred_at, event_id)`.
2. Event IDs within a Scenario are unique.
3. A transition consumes exactly the state produced by the previous transition.
4. The initial State is never mutated.
5. The final State is the terminal state of the transition chain.
6. A transition records the event and before/after state-property changes.
7. The same Scenario and seed produce the same run and run ID.
8. The chain is machine-readable through `SimulationRun.to_dict()` and `canonical_payload()`.

## Scope

S6 does not yet generate downstream events from `CAUSES`, calculate KPI/Risk propagation, perform stochastic simulation, optimize decisions, or require Neo4j. Those concerns build on this deterministic chain contract.

## Contract

`SimulationKernel.run(scenario)`:

1. Sorts events by `(occurred_at, event_id)`.
2. Rejects duplicate event IDs.
3. Applies each event to the current state.
4. Records the resulting Transition.
5. Validates chain connectivity before returning `SimulationRun`.

`SimulationRun.validate_transition_chain()` verifies that transition `i` starts from the state produced by transition `i-1`, that event and transition order agree, and that the terminal transition reaches `final_state`.

## Example

```text
Supplier A leadTimeDays = 5

SUPPLIER_DELAY +7d
        |
        v
State₁: leadTimeDays = 12
        |
SUPPLIER_DELAY +2d
        |
        v
State₂: leadTimeDays = 14
```

This is deliberately a small semantic kernel. More domain-specific propagation will be introduced only after the chain contract is stable.
