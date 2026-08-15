# S159 — Unified Canonical Assertion Model

S159 consolidates contextual assertions about entity attributes and relations into one assertion contract.

## Model

```text
Canonical Entity ── Attribute ── Value
                         │
                         └── EntityAssertion

Canonical Entity ── Relation ── Canonical Entity
                         │
                         └── RelationAssertion

EntityAssertion / RelationAssertion
                 ↓
         Assertion Context
      ├─ Temporal
      ├─ Epistemic
      └─ Provenance
```

## Core invariants

1. Every assertion has a unique assertion reference within an assertion set.
2. Entity assertions bind their context to the same assertion and subject.
3. Relation assertions bind their context to the same relation.
4. Null is not silently converted into a canonical value.
5. Temporal, epistemic, and provenance semantics remain context dimensions rather than being embedded into the value itself.

## Architectural role

```text
Canonical Schema
      ↓
Core Instance Model
      ↓
Canonical Assertion Model
      ↓
Graph / JSON / RDF / persistence adapters
```

This is the consolidation point before serialization and graph adapters. It does not introduce storage semantics or reasoning behavior.

## Non-goals

No graph database implementation, inference, metric calculation, enterprise mapping, or automatic identity resolution.
