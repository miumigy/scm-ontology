# S125 — Provenance Graph

## Purpose

S125 defines how S104 Provenance / Lineage semantics are projected into the SCM Graph established by S123 and extended temporally by S124.

The graph must answer:

> Where did this value, metric, assessment, or decision come from?

## Canonical provenance chain

```text
Source
  ↓
Evidence
  ↓
Observation / Assertion
  ↓
Transformation / Derivation
  ↓
Canonical Value
  ↓
Metric / Assessment
  ↓
Decision
```

A provenance edge identifies a semantic dependency; it does not imply that the upstream object is true merely because it is a source.

## Core provenance relations

- `supported_by`
- `derived_from`
- `transformed_from`
- `asserted_from`
- `measured_from`
- `evaluated_from`
- `decided_from`
- `sourced_from`

The relation predicate must remain explicit. A generic `related_to` edge is insufficient for explainability.

## Source authority vs truth

`Source Authority` describes the authority or reliability assigned to a source in context. It is not equivalent to truth.

```text
Source
  + authority
  + evidence
  + observation time
  + transaction time
        ↓
Provenance
```

## Transformation preservation

A transformation must remain inspectable:

```text
source value
   ↓ transformation
intermediate value
   ↓ derivation
canonical value
```

The canonical value must not erase the source value, mapping reference, transformation kind, or relevant temporal context.

## Epistemic integration

Provenance and epistemic status are complementary.

```text
Evidence → Observation → Inference
```

An inferred value remains an inference even when its provenance chain is complete. Provenance completeness does not upgrade epistemic status.

## Temporal integration

Every provenance assertion may need temporal context. At minimum, the graph must be capable of distinguishing:

- when a source assertion was valid/effective
- when it was recorded/received
- when it was observed
- when a transformation was performed

S124 temporal semantics remain authoritative.

## Decision explainability

A decision should be traversable backwards to the evidence and canonical facts/measurements used to support it:

```text
Decision
  ↓ decided_from
Assessment / Metric
  ↓ evaluated_from
Canonical Measurement
  ↓ derived_from / measured_from
Observation
  ↓ supported_by
Evidence / Source
```

This enables evidence-oriented explanations without embedding explanation prose into the Core Ontology.

## Provenance completeness

A provenance chain can be incomplete. Missing provenance must be represented as missing/unknown, not fabricated.

```text
Unknown provenance ≠ no provenance
Unknown provenance ≠ trustworthy provenance
```

## Non-goals

S125 does not define:

- a particular graph database
- cryptographic data lineage
- enterprise audit policy
- source ranking algorithms
- AI explanation templates

Those are implementation or governance layers above the canonical semantics.
