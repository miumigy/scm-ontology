# S16 — Observation Provenance Contract

## Canonical meaning

`MetricObservation.source_ref` identifies the information source from which an observation is derived or recorded.

## Contract

- `source_ref` MUST be a non-empty string.
- The ontology does not prescribe a URI scheme or vendor-specific source model.
- Provenance identifies the source reference; it does not assert that the source is authoritative.
- Source systems, ingestion mechanisms, and lineage graphs remain outside this contract.

## Semantic boundary

S16 does not introduce a new Source entity or an `Observation -> Source` relationship. The existing `source_ref` field is sufficient for the current canonical observation model.
