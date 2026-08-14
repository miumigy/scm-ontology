# S84 — Observation Provenance Semantics

S84 defines the semantic boundary between an Observation and the provenance of the information used to create, record, transmit, or derive it.

## Canonical decision

Provenance is **not** added as fields to the canonical Observation primitive and is **not** treated as Evidence.

The current Observation remains:

```text
Observation
├─ observation_id
├─ observed_at
└─ subject_id
```

Provenance is a separate semantic layer describing the history or origin of an information artifact or assertion.

## Core distinction

```text
Observation
    = what was observed, with its subject and observation time

Provenance
    = how / where / by whom / through what activity the information was produced or derived

Evidence
    = an epistemic role in supporting or challenging a Claim

Source Record
    = identity of a record in a source system
```

These concepts are related but not interchangeable.

```text
Provenance ≠ Evidence
Provenance ≠ Observation
Provenance ≠ Source Record
```

## Example

An application may have:

```text
Observation
  observation_id = OBS-001
  subject_id     = WH-A
  observed_at    = 10:00
```

and separately know that:

```text
Provenance
  source_system  = WMS
  source_record  = INV-123
  activity       = inventory_snapshot_export
  agent          = WMS service
  generated_at   = 10:01
```

The provenance explains how the information was obtained or produced; it does not change the Observation's identity or observed time.

## Source record boundary

A source record may be the provenance source for an Observation, but source-record identity is not Observation identity.

```text
WMS:INV-123
      │
      │ provenance/source relation
      ▼
Observation: OBS-001
```

This relationship does not imply that every source record is itself an Observation, nor that every Observation must have exactly one source record.

Multiple source records may contribute to a derived Observation, and one source record may support multiple semantic objects.

## Evidence boundary

Evidence and Provenance answer different questions:

```text
Evidence
  → Why should a Claim be supported or challenged?

Provenance
  → Where did this information come from and through what process?
```

A provenance-bearing source record may also be used as Evidence, but neither role subsumes the other.

For example:

```text
Source Record
   │
   ├── provenance ──→ Observation
   │
   └── evidence ────→ Claim
```

The existence of provenance does not establish truth, and the existence of Evidence does not establish a particular provenance chain.

## Temporal boundary

`observed_at` is the time of the observation in domain semantics. Provenance timestamps such as ingestion, transformation, export, registration, or publication time are distinct temporal facts.

```text
observed_at
    ≠ generated_at
    ≠ ingested_at
    ≠ published_at
```

S84 does not prescribe a canonical timestamp vocabulary for all provenance activities.

## Canonical scope

S84 deliberately does not introduce a mandatory `Provenance` entity, `Source`, `Agent`, or `Activity` hierarchy. Those may become explicit primitives if repeated cross-domain requirements demonstrate a stable need.

Until then, provenance can be represented by a dedicated provenance/data-lineage layer without changing the core Observation contract.

## Non-goals

S84 does not define a provenance graph schema, source-system registry, agent ontology, activity vocabulary, data-lineage implementation, automatic provenance extraction, or truth/confidence model.
