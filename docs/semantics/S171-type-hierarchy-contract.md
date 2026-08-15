# S171 — Explicit Type Hierarchy Contract

S171 introduces a deliberately small canonical type hierarchy so future relation validation can distinguish direct type matching from explicit subtype compatibility.

## Contract

```text
Facility → Node → Location → Entity
KPI      → Metric → Entity
Product  → PhysicalEntity → Entity
```

The hierarchy is explicit and versioned in code. Unknown types are not silently coerced into canonical types.

## Boundary

S171 does **not** change relation validation to perform transitive subclass inference yet. That is intentionally deferred so the distinction between:

- direct domain/range match
- explicit subtype compatibility
- inferred semantic compatibility

remains visible and testable.

This prevents accidental ontology expansion through implicit type assumptions.
