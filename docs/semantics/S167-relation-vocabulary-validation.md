# S167 — Relation Vocabulary Validation

S167 closes the gap between the canonical relation registry and runtime relation instances.

```text
Canonical Relation Registry
        ↓
Canonical Predicate Vocabulary
        ↓
CanonicalRelation
        ↓
Vocabulary Validation
```

A `CanonicalRelation` must use a predicate registered by S165. Unknown or enterprise-specific predicates are rejected at the canonical validation boundary.

## Boundary

This validates vocabulary membership only. It does not infer subject/object types, cardinality, inverse facts, causality, or business-process semantics.

Those concerns remain separate semantic validation layers.
