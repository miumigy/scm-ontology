# S86 — Observation Temporal Semantics

S86 defines the canonical meaning of time in an Observation and separates observation time from recording, ingestion, publication, and derivation times.

## Canonical decision

`observed_at` is the canonical temporal attribute of the Observation primitive.

```text
Observation
├─ observation_id
├─ observed_at   ← domain observation time
└─ subject_id
```

`observed_at` means the time at which the subject was observed in the domain semantics. It is not a generic system timestamp.

The Observation primitive does not add `recorded_at`, `ingested_at`, `published_at`, `generated_at`, or `effective_at` fields.

## Temporal boundaries

The following timestamps represent different semantic questions:

```text
observed_at  = when the observation occurred / was observed
recorded_at  = when a source system recorded the information
ingested_at  = when another system ingested the information
published_at = when the information was made available to consumers
generated_at = when a derived artifact or result was generated
```

Therefore:

```text
observed_at
    ≠ recorded_at
    ≠ ingested_at
    ≠ published_at
    ≠ generated_at
```

A concrete implementation may retain these additional timestamps in its provenance, lineage, or application layer.

## Point observations

A point Observation has one canonical observation instant:

```text
Observation O1
  observed_at = 10:00
```

The precision of the timestamp is part of the source/application semantics. S86 does not define a universal precision or rounding rule.

## Intervals

S86 does not add `valid_from` / `valid_to` to the canonical Observation primitive.

When the domain requires interval semantics, an application may represent the interval through a separate temporal semantic layer or domain-specific contract.

This avoids assuming that every Observation describes a state valid throughout an interval merely because the source stores effective dates.

## Forecasts and plans

A generated forecast or plan has multiple temporal concepts that must not be collapsed into `observed_at`.

For example:

```text
forecast generated_at = 10:00
forecast target period = 18:00–20:00
```

The generation time belongs to provenance/derivation semantics, while the target period belongs to the forecast/plan domain semantics.

A forecast result must not use `observed_at` merely because it is represented using an Observation-shaped object.

## Derived observations

S85 establishes that a derived Observation is still an Observation, with its own identity. S86 adds that its `observed_at` must retain its domain meaning.

For example, if a reconciliation process at 10:05 produces an Observation describing the state determined for 10:00:

```text
observed_at  = 10:00
recorded_at  = 10:05
```

The derivation/recording time must not overwrite the observation time.

## Timezone and precision

S86 does not define a universal timezone, calendar, timestamp precision, or clock-synchronization protocol. Implementations must preserve enough temporal information to interpret `observed_at` correctly in their domain context.

## Non-goals

S86 does not define an interval ontology, temporal database model, clock synchronization mechanism, timezone registry, forecast period model, planning horizon model, or provenance timestamp vocabulary.
