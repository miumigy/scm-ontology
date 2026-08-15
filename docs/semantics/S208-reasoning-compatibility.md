# S208 — Reasoning Compatibility

S208 defines the minimum registry invariants required before canonical relations are consumed by a reasoning layer.

```text
Canonical Relation Registry
          ↓
Reasoning Compatibility
          ├─ unique predicates
          └─ reciprocal declared inverses
          ↓
Reasoning-safe relation vocabulary
```

Undeclared inverse references remain permitted for backward compatibility with the canonical registry model. If both sides of an inverse pair are declared, they must be reciprocal.

This validation is read-only and does not execute inference or mutate graph state.
