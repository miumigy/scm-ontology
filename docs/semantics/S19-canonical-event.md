# S19 — Canonical Event Semantics

## Definition

A **CanonicalEvent** represents an occurrence associated with a canonical entity at a defined instant.

It is distinct from:

- **MetricObservation** — a measured fact
- **CanonicalState** — a condition or configuration holding over a period

## Minimal contract

```text
CanonicalEvent
├─ event_type
├─ occurred_at
├─ entity_id
└─ attributes
```

`occurred_at` is a timezone-aware instant, consistent with the temporal semantics established for observations.

## Explicit non-goals

The core ontology does not prescribe:

- SCM-specific event vocabularies
- event lifecycle/state machines
- causal relationships such as Event → State
- automatic Observation → Event inference
- source-system-specific event identifiers

Those semantics belong in mapping, enterprise, or application layers unless later promoted to canonical principles.
