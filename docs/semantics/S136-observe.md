# S136 — Observe

S136 defines the SCM OS Observe semantic: acquiring knowledge about the supply chain without conflating the observation with the underlying world state.

## Observe contract

```text
Source
  ↓
Observation
  ↓
Measurement (when applicable)
  ↓
Epistemic Assessment
  ↓
State Reconstruction / Update
```

Observation is a record of an observation; it is not automatically the state itself.

## Boundaries

- Observation ≠ Event
- Observation ≠ State
- Measurement ≠ Metric
- Observation ≠ Fact
- Observation ≠ Inference
- Source ≠ Observation

An observation can report an event, measure a state, or provide evidence about a claim, but those semantic objects remain distinct.

## Observation context

An observation should preserve, where applicable:

- observed subject
- observation time
- source reference
- observed value or content
- observation method
- unit of measure when applicable
- uncertainty
- provenance
- source identity

## Measurement connection

A quantitative observation may produce a Measurement. Measurement semantics from S112 remain authoritative for units, methods, uncertainty, and source.

```text
Observation
    ↓ produces / records
Measurement
    ↓ contributes to
Metric
```

The observation does not become a Metric merely because it contains a number.

## State connection

Observation may provide evidence for reconstructing State in S135. It must not silently overwrite historical state or convert uncertainty into certainty.

```text
Observation
    ↓ evidence_for
State Reconstruction
```

## Epistemic preservation

Observe records what is known from a source at a given observation time. If the source reports an estimate or prediction, that epistemic status is preserved rather than promoted to actual fact.

## Missing and stale observations

Missing data and stale data are semantic conditions, not zero values. A consumer may derive a State or Metric with a corresponding uncertainty or validity assessment.

## Provenance

Every observation should retain source/provenance references whenever available. This allows downstream State, Metric, Decision, and Explanation objects to trace back to the original observation.

## Non-goals

S136 does not define connectors, polling schedules, event streaming, IoT protocols, database ingestion, or UI behavior. It defines the canonical meaning of observation independent of acquisition technology.
