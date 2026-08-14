# S68 — Observation Semantics

## Purpose

S68 introduces the smallest canonical observation primitive needed to distinguish when a semantic subject was observed from when a claim is valid.

## Canonical form

```text
Observation
├─ observation_id
├─ observed_at
└─ subject_id
```

`observed_at` identifies the time at which the observation occurred. `subject_id` identifies the semantic subject being observed.

## Boundary

Observation is not a claim, fact, evidence reference, event, or provenance record.

```text
Observation
    ≠ Claim
    ≠ Fact
    ≠ Evidence
    ≠ Event
    ≠ Provenance
```

In particular:

- **Event time** describes when an event occurs.
- **Observation time** describes when a subject/state is observed.
- **Claim validity** describes when a claim applies or is true.
- **Evidence reference** identifies supporting material.
- **Assertion/provenance time** describes when a claim or derivation was asserted or produced; it is not introduced by S68.

## Scope limits

S68 intentionally does not define:

- timezone policy
- clock precision
- observation value schema
- sensor/device modeling
- observation methodology
- event/observation equivalence
- observation validity intervals
- persistence or audit storage

The primitive is a semantic anchor for observation time and subject identity, not an implementation of an observation system.
