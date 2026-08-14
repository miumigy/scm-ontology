# S80 — Observation Semantics

S80 defines the minimum canonical semantics of `Observation` without collapsing Observation into Claim or introducing a second assertion model.

## Canonical decision

Observation remains a temporal reference to something observed about a subject:

```text
Observation
├─ observation_id
├─ observed_at
└─ subject_id
```

The current primitive intentionally does not add `value`, `predicate`, or `object` fields. The Observation primitive therefore remains distinct from Claim, whose canonical form is subject–predicate–object.

## Why no predicate/object on Observation

A predicate/object pair would make Observation structurally resemble Claim:

```text
subject ─ predicate ─ object
```

That would blur the distinction between:

- an occurrence of observation, and
- an assertion about what was observed.

Observation answers **when and to whom/what an observation occurred**. Claim answers **what proposition is being asserted**.

## Why no generic value field

A generic `value` field appears attractive for measurements, status observations, counts, and similar use cases, but it would force a single representation for heterogeneous observed phenomena and invite implementation-specific typing.

Values and observed phenomena can be modeled by domain-specific primitives or semantic relationships without changing the canonical Observation identity contract.

## Temporal semantics

`observed_at` is part of the Observation identity semantics. It represents the time at which the observation occurred, not the time at which a source system recorded, imported, or published the evidence.

Those lifecycle/provenance times remain separate concerns.

## Relationship to Claim

An Observation may provide Evidence for a Claim, but no automatic Claim is inferred from an Observation.

```text
Observation
    │ may be represented/referenced as Evidence
    ▼
Evidence
    │ supports / contradicts / corroborates / qualifies
    ▼
Claim
```

Thus:

```text
Observation ≠ Claim
```

## Relationship to measurement

A measurement may be represented using an Observation, but `Observation` is not defined as a measurement-only primitive. The model remains capable of representing observations of state, event occurrence, status, or other phenomena.

## Non-goals

S80 does not add `value`, `predicate`, `object`, measurement units, confidence, source timestamp, automatic inference, or an Observation subtype hierarchy.
