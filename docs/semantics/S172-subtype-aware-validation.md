# S172 — Subtype-Aware Relation Validation

S172 connects the explicit S171 type hierarchy to relation domain/range validation.

## Contract

A relation instance is compatible when its actual subject/object type is equal to, or an explicitly registered subtype of, one of the canonical domain/range types.

```text
Facility
  ↓ subtype
Node
  ↓ subtype
Location

located_at(PhysicalEntity, Facility)
        ✓ compatible with Range = Location | Node
```

## Important boundary

Only the registered canonical hierarchy is traversed. Unknown types are rejected; no structural similarity or source-system naming convention is used as implicit subtype evidence.

This is **type compatibility**, not semantic inference. It does not infer new relations, cardinality, causality, or business meaning.
