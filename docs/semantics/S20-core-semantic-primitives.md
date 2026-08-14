# S20 — Core Semantic Primitives Consolidation

S20 consolidates the semantic boundaries established through S10–S19 into one reference surface. It is a semantic baseline, not a new domain model.

## Core primitives

- Entity — canonical identifiable thing.
- MetricDefinition — meaning and interpretation of a metric.
- MetricObservation — measured fact with entity context, time, and provenance.
- CanonicalState — condition or configuration that holds.
- CanonicalEvent — occurrence associated with an entity at an instant.
- Impact — explicit effect/influence semantics.
- Target — explicit object/scope of an impact.
- Provenance — origin reference for an observation.
- Time — temporal semantics represented by timezone-aware instants.

## Fundamental distinctions

```text
MetricDefinition ≠ MetricObservation
Observation ≠ State
Observation ≠ Event
State ≠ Event
Provenance ≠ Source Entity
Instant ≠ Time Entity
Impact ≠ relationship-wide causality
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

## Design principles

1. Prefer semantic contracts over redundant graph nodes.
2. Keep Core framework-independent and SCM-domain-vocabulary-light.
3. Separate facts, conditions, and occurrences.
4. Keep provenance explicit without over-modeling source systems.
5. Treat time as temporal semantics unless a richer temporal entity is explicitly required.
6. Keep causal, lifecycle, mapping, ingestion, and enterprise-specific semantics outside Core until promoted deliberately.

## Scope of S20

S20 consolidates existing semantics. It intentionally does **not** add a new Entity, Relationship family, State transition model, Event vocabulary, or reasoning rule.

**Canonical baseline:** SCM Ontology v0.2.
