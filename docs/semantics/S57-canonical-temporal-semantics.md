# S57 — Canonical Temporal Semantics

## Status

Semantic Contract implemented as minimal temporal primitives.

## Purpose

Separate the semantic meaning of time from timestamp syntax, persistence, and interval computation.

## Core distinction

SCM temporal references have different semantic roles.

```text
Event
  └─ occurrence
       └─ point

Relationship / State
  └─ validity
       └─ interval
```

An Event answers **when an occurrence happened**.
A validity assertion answers **during which interval a condition or relationship holds**.

These meanings must not be collapsed into a single generic `valid_from` field.

## Canonical primitive

```text
TemporalReference
├─ kind: point | interval
├─ start
└─ end: optional
```

A point has only `start`.
An interval has `start` and may omit `end` for an open-ended interval.

The temporal literals are opaque to this contract. Parsing, calendar semantics, timezone policy, precision, and interval arithmetic are implementation concerns for later contracts.

## TemporalAssertion

```text
TemporalAssertion
├─ role: occurrence | validity
└─ reference: TemporalReference
```

Canonical compatibility rules:

- `occurrence` requires a `point` reference.
- `validity` requires an `interval` reference.

## Relationship to S46

S46 `valid_from` / `valid_to` represent Relationship Version validity. S57 does not replace that contract; it generalizes the semantic notion of a validity interval so that State validity can use the same primitive without forcing Event occurrence into the same model.

## Event boundary

S56 defines Event as an occurrence. S57 supplies the temporal role that can be attached to an Event:

```text
Event-1
  occurrence = 2026-08-14T09:00:00
```

The Event primitive itself does not acquire mandatory timestamp fields.

## State boundary

A State is a condition/configuration that holds for a subject. S57 provides a validity interval for that condition:

```text
State-1
  validity = [2026-07-01, null)
```

The State primitive remains free of mandatory temporal fields.

## What S57 intentionally excludes

- timestamp parsing
- timezone policy
- calendar systems
- interval arithmetic
- transaction-time semantics
- audit time
- persistence temporal tables
- event sourcing
- temporal databases
- automatic temporal inference

## Canonical boundary

```text
Temporal semantics
      ≠
timestamp serialization
      ≠
database temporal schema
      ≠
transaction-time/audit model
      ≠
interval computation engine
```

The goal is to establish **what a temporal reference means**, not how a particular system stores or calculates it.
