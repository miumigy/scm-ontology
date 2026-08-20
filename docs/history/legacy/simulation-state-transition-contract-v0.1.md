# SCM Simulation State Transition Contract v0.1

> Historical S5 simulation contract. Archived after M8 completion.

## Purpose

S5 makes the state change caused by a simulation event explicit and deterministic.

The canonical semantic boundary is:

```text
Event
  ↓
StateTransitionRule
  ↓
Transition
  ↓
New State
```

The event does not mutate a state directly.

## Canonical property example

The first S5 rule uses the existing canonical supplier property `leadTimeDays`.

```text
Supplier A
leadTimeDays = 5

SUPPLIER_DELAY
magnitudeDays = 7

→ leadTimeDays = 12
```

The property remains a canonical state value. `StateTransitionRule` is simulation runtime metadata describing how a canonical state changes in response to an event.

## Rule contract

A rule contains `ruleId`, `eventType`, `entityType`, `propertyName`, and `attributeName`.

S5 currently supports a non-negative integer increment for the mapped property.

## Invariants

1. Applying the same state, event, and rule produces the same state and change set.
2. The input state is never mutated.
3. The rule must match the event type.
4. The target entity must have the expected canonical entity type.
5. The source property and event magnitude must be non-negative integers.
6. The rule is not tied to a specific entity ID.

## Relationship to S4

S4 establishes causal lineage:

```text
Event → CausalRule → Derived Event
```

S5 establishes state change:

```text
Event → StateTransitionRule → New State
```

These are intentionally separate contracts. A causal relationship does not automatically imply a state mutation.
