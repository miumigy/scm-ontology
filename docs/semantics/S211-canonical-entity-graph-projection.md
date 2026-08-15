# S211 — Canonical Entity Graph Projection

S211 introduces the read-only boundary from canonical entity records to immutable graph-node descriptors.

```text
Canonical Entity
  ├─ type
  ├─ id
  └─ properties
       ↓
Entity Graph Projection
       ↓
CanonicalEntityGraphNode
```

`id` is the stable graph identity. Entity properties are carried as deterministic key/value pairs, while identity is represented separately from mutable attributes.

The projection does not write to a graph store and does not mutate canonical entities or the registry.
