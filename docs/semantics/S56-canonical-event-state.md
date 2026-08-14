# S56 — Canonical Event / State Model

## Status

Semantic Contract draft implemented as minimal canonical primitives.

## Purpose

Introduce SCM-native Event and State concepts without coupling them to a database schema, temporal persistence model, or causal engine.

## Event

An **Event** is an occurrence in the SCM domain.

```text
CanonicalEvent
├─ event_id
└─ event_type
```

`event_id` identifies the particular occurrence. `event_type` identifies its semantic kind.

An Event does not itself contain:

- a State transition
- a causal rule
- persistence metadata
- audit-log fields
- mandatory timestamp policy

Those semantics are represented by separate contracts.

## State

A **State** is a condition or configuration that holds for a canonical subject.

```text
CanonicalState
├─ state_id
├─ state_type
└─ subject_id
```

`subject_id` identifies the canonical object whose condition is represented.

A State does not itself contain:

- the Event that established it
- temporal validity fields
- persistence/version fields
- a causal explanation

## Event vs State

```text
Event = an occurrence
State = a condition/configuration that holds
```

Example:

```text
Event
  shipment_departed

State
  Shipment-1 : in_transit
```

The semantic connection between them is expressed through Relationship predicates or a future transition contract; it is not embedded in either primitive.

## Relationship boundary

Existing relationship semantics remain the canonical mechanism for connections such as:

```text
Event ──changes──→ State
Event ──establishes──→ State
```

The exact endpoint constraints and predicate vocabulary remain governed by their existing contracts.

## Temporal boundary

S56 intentionally does not define `occurred_at`, `valid_from`, `valid_to`, interval arithmetic, timezone policy, or persistence versioning. Those belong to a dedicated temporal contract and must remain compatible with S46 Relationship Version / Validity.

## Causal boundary

S56 does not define causal inference. A causal or transition relation may connect Events and States, while inference rules remain in the S52–S54 reasoning layer.

## Canonical boundary

```text
Event / State semantics
        ≠
relationship implementation
        ≠
database event table
        ≠
audit log
        ≠
event sourcing
        ≠
causal engine
```

## Design principle

Event and State are semantic primitives. Their relationships, temporal semantics, causal semantics, persistence, and execution behavior should be composed by separate contracts rather than absorbed into the primitives.
