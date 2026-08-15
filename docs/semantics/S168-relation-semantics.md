# S168 — Relation Semantic Classification

S168 makes the semantic class of a canonical predicate programmatically discoverable.

## Contract

```text
predicate_ref
    ↓
Canonical Relation Registry
    ↓
RelationKind
```

The helper layer exposes classification for consumers such as graph adapters and validation without changing the assertion model.

## Important boundary

Classification is descriptive, not inferential.

- `causes` and `results_in` are causal predicates.
- `fulfills` and `supplies` are operational predicates.
- `located_at` is physical, not causal.
- An operational relationship must not be promoted to causality merely because it participates in a business process.

Unknown predicates are rejected rather than silently classified.

S168 does not introduce cardinality, domain/range typing, inverse fact generation, or reasoning rules.
