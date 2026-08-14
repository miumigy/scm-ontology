# S36 — Canonical State Concept

## Definition

**State** is the effective condition of a subject at a defined point in time.

## Minimal concept contract

```text
CanonicalState
├─ state_type
├─ subject_id
└─ effective_at
```

State describes a condition, not an occurrence. A subject can have many historical states and one or more effective states depending on the context and state model.

## Fundamental boundaries

```text
State  ≠ Event
State  ≠ Entity
State  ≠ Relationship
```

An Event records that something happened. A State represents the condition resulting from or otherwise established by business semantics.

## Example

```text
Shipment
   │
   ├─ Event: departed @ 09:30
   ├─ State: in_transit @ 09:30
   ├─ Event: arrived  @ 14:10
   └─ State: arrived   @ 14:10
```

The mapping from Event to State is intentionally not implicit in S36.

## State vocabulary

Possible scoped state values include:

```text
Order:       draft / confirmed / cancelled / fulfilled
Shipment:    planned / dispatched / in_transit / arrived
Production:  planned / released / running / completed
Inventory:   available / reserved / blocked
```

These are vocabulary examples, not universal canonical enums.

## Non-goals

S36 does not define:

- state machines
- valid transitions
- transition causality
- event-to-state derivation
- temporal validity intervals
- concurrency rules
- state ownership
- process-specific lifecycle semantics

Those require later contracts.

## Graph impact

S36 adds the condition layer to the SCM Graph:

```text
Subject
  ├─ Event  ──occurred_at──→ Time
  └─ State  ──effective_at─→ Time
```

This preserves the distinction between **what happened** and **what is currently true**.
