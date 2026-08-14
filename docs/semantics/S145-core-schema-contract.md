# S145 — Core Schema Contract

S145 freezes the first machine-readable serialization contract for the canonical SCM model without yet choosing JSON-LD, OWL, RDF, or a graph database implementation.

## Purpose

S113–S144 established and reconciled the semantic model. S145 defines the minimum structural contract that a future serializer must preserve.

```text
Canonical Concept
  ├─ name
  ├─ layer
  ├─ world(s)
  ├─ description
  └─ abstract?

Canonical Relationship
  ├─ predicate
  ├─ source
  ├─ target
  └─ category
```

## Serialization invariants

A conforming machine-readable representation MUST preserve:

1. unique canonical concept identity by name;
2. explicit concept layer: primitive, core, derived, contextual;
3. explicit world classification;
4. relationship predicate, source, target, and category;
5. relationship endpoint resolvability;
6. derived concepts as derived rather than silently promoted to core;
7. semantic distinction between planned, scheduled, committed, executed, and actual states;
8. provenance, temporal, epistemic, scenario, causal, and learning references when represented by the source model.

## Identity

Concept names are canonical semantic identifiers within the current registry. They are not enterprise source-system identifiers.

Future namespaces or IRIs may be introduced, but must not change the semantic identity of an existing concept.

## Relation semantics

Relationships are first-class semantic declarations. A serializer must not flatten them into arbitrary implementation-specific foreign keys.

For example:

```text
Recommendation --informs--> Decision
Decision       --authorized_by--> Action
Action         --execution_of--> Execution
Execution      --results_in--> Outcome
LearningResult --updates--> Policy / Rule / Model / Knowledge
```

## Primitive vs derived

The schema contract must preserve the distinction between canonical state-bearing concepts and computed concepts.

Examples:

```text
Inventory          → Core
Measurement        → Core
MetricValue        → Core
KPI                → Derived
PerformanceAssessment → Derived
Variance           → Derived
RiskScore          → Derived
```

A derived metric can be serialized, queried, and versioned, but its derived status remains explicit.

## World layers

The current model distinguishes:

- Physical
- Information
- Decision
- Semantic

These are semantic classifications, not four disconnected schemas. Cross-world relationships remain valid where the ontology defines them.

## Non-goals

S145 does not:

- select JSON-LD, RDF, OWL, or another serialization standard;
- define database tables;
- define graph storage;
- define SHACL/cardinality constraints;
- add enterprise-specific mappings;
- introduce new SCM business concepts merely for serialization convenience.

## Acceptance criterion

A future serializer is acceptable only if a round-trip through the chosen machine-readable representation preserves the S145 invariants and produces an equivalent canonical semantic registry.
