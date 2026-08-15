# S176 — Relation Registry Consistency

S176 adds regression guards around the relationship between the canonical predicate registry and its domain/range constraint registry.

## Contract

Every constrained predicate must first exist in the canonical predicate registry.

Inverse references remain navigational metadata and do not automatically require a corresponding constraint or assertion.

```text
Canonical Relation Registry
        ↓
Domain / Range Constraint Registry
        ↓
Validation Pipeline
```

The constraint registry may intentionally cover only predicates for which canonical typing is currently mature. This avoids forcing premature domain/range commitments for every predicate.
