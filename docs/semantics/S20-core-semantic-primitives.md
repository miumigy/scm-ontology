# S20 — Core Semantic Primitives Consolidation

## Purpose

S20 consolidates the semantic boundaries established through S10–S19 into one reference surface. It is a semantic baseline, not a new domain model.

## Core primitives

| Primitive | Meaning | Core boundary |
|---|---|---|
| Entity | Canonical identifiable thing | Identity is semantic, not a source-record alias |
| MetricDefinition | Meaning of a metric | Definition is distinct from measured value |
| MetricObservation | Measured fact | Has metric, value, entity context, time, and provenance; does not imply State/Event |
| CanonicalState | Condition/configuration that holds | Not an occurrence |
| CanonicalEvent | Occurrence | Not a persistent condition |
| Impact | Effect/influence semantics | Propagation is explicit, not implicit on every relation |
| Target | Object/scope of an impact | Requires explicit impact relation |
| Provenance | Origin reference | Does not require a canonical Source entity or authority claim |
| Time | Instant semantics | Represented by timezone-aware timestamps; no redundant Time node |

## Fundamental distinctions

```text
MetricDefinition  ≠ MetricObservation
Observation       ≠ State
Observation       ≠ Event
State             ≠ Event
Provenance        ≠ Source Entity
Instant           ≠ Time Entity
Impact            ≠ Relationship-wide causality
```

## Canonical observation context

```text
MetricObservation
├─ metric_id
├─ value
├─ observed_for → Entity
├─ observed_at  → timezone-aware instant
└─ source_ref   → provenance reference
```

## State / Event boundary

```text
Observation = measured fact
State       = condition / configuration
Event       = occurrence
```

The Core Ontology does not automatically infer State or Event from an Observation, nor does it prescribe Event → State causality.

## Design principles locked by S20

1. Prefer semantic contracts over redundant graph nodes.
2. Keep Core framework-independent and SCM-domain-vocabulary-light.
3. Separate facts, conditions, and occurrences.
4. Make provenance explicit without over-modeling source systems.
5. Treat time as temporal semantics unless a domain requires a richer temporal entity.
6. Keep causal, lifecycle, mapping, ingestion, and enterprise-specific semantics outside Core until explicitly promoted.

## Scope of S20

S20 consolidates existing semantics. It intentionally does **not** add a new Entity, Relationship family, State transition model, Event vocabulary, or reasoning rule.
