# S37 — Event → State Transition Relationship Contract

## Purpose

S37 makes the semantic bridge between temporal facts and effective conditions explicit.

## Canonical contract

```text
EventStateTransition
├─ event_type
├─ predicate
└─ state_type
```

Initial canonical transitions:

```text
shipment_departed   ──establishes──→ in_transit
shipment_arrived    ──establishes──→ arrived
order_confirmed     ──establishes──→ confirmed
production_started  ──establishes──→ running
production_completed──establishes──→ completed
```

## Critical boundary

S37 defines a **semantic relationship**, not a universal state machine.

An event type may establish a state in one business context without implying that every occurrence automatically changes the current state in every implementation.

Likewise, a state may be established by multiple event types or by non-event business rules.

## Direction

```text
Event ──establishes──→ State
```

The direction expresses semantic effect, not necessarily physical causality or implementation order.

## Event vs State

```text
Shipment
  │
  ├─ Event: shipment_departed @ T1
  │       │
  │       └─ establishes → State: in_transit
  │
  ├─ Event: shipment_arrived @ T2
  │       │
  │       └─ establishes → State: arrived
  │
  └─ Current State: arrived
```

The transition contract does not store the subject or event timestamp. Those belong to the Event and State instances.

## Non-goals

S37 does not define:

- exhaustive state machines
- allowed/disallowed transitions
- rollback semantics
- event ordering
- concurrency
- state precedence
- automatic derivation algorithms
- implementation event sourcing
- process-specific lifecycle rules

Those remain separate contracts.

## Graph impact

S37 completes the minimal temporal semantic chain:

```text
Event
  │
  │ establishes
  ▼
State
  │
  ▼
Current condition of Subject
```

This provides a reusable foundation for Order, Shipment, Production, and Inventory lifecycle semantics without coupling their domain-specific state machines to the canonical ontology layer.
