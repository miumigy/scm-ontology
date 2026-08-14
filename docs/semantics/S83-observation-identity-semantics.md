# S83 — Observation Identity Semantics

S83 defines the identity boundary for the canonical Observation primitive and separates ontology identity from real-world observation equivalence and source-record identity.

## Canonical decision

`observation_id` is the canonical identity of an Observation instance.

```text
Observation
├─ observation_id  ← canonical identity
├─ observed_at
└─ subject_id
```

`subject_id` and `observed_at` are semantic attributes, not a composite identity key. Two observations with the same subject and timestamp may still be distinct Observation instances.

## Identity is not equivalence

The following concepts are distinct:

```text
Observation identity
    = identity of an ontology instance

Real-world observation equivalence
    = a judgment that two observations represent the same underlying observation

Source-record identity
    = identity assigned by WMS / ERP / IoT / sensor / other source
```

S83 does not make these equivalent.

For example:

```text
OBS-001  WH-A  10:00
OBS-002  WH-A  10:00
```

are two distinct Observation instances unless an explicit reconciliation process establishes an equivalence relationship.

Likewise, identical source records from two systems do not automatically become one canonical Observation.

## No natural-key inference

The combination:

```text
subject_id + observed_at
```

must not be used by the canonical model as an implicit identity key.

This is important because multiple observations may legitimately occur at the same timestamp for the same subject, and because source timestamp precision may differ.

## Source records and reconciliation

A source system may assign its own record identifier:

```text
WMS:INV-123
ERP:STOCK-456
IoT:SENSOR-789
```

Those identifiers are source-record identities. They do not replace `observation_id` and do not automatically establish identity equivalence.

A future reconciliation or entity-resolution layer may assert that two Observation instances are equivalent, related, duplicated, superseded, or derived from the same source event. Such assertions are separate semantics from Observation identity.

## Temporal semantics

`observed_at` identifies when the observation occurred or was observed in the domain semantics. It is not an identity component and must not be interpreted as ingestion time, registration time, publication time, or source-system processing time.

## Relationship to Evidence

An Observation may be referenced or represented as Evidence, but Evidence identity remains separate. A source record used as evidence does not automatically establish Observation identity.

```text
Observation identity
    ≠ Evidence identity
    ≠ Source-record identity
```

## Non-goals

S83 does not define duplicate detection, entity resolution algorithms, fuzzy matching, source-record reconciliation, event deduplication, temporal tolerance windows, or automatic identity merging.
