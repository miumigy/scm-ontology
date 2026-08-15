# S207 — Registry Graph Projection

S207 defines a read-only projection from canonical relation declarations to graph-edge descriptors.

```text
Canonical Relation Registry
          ↓
  Graph Projection
          ↓
RegistryGraphEdge*
```

The projection preserves predicate and endpoint type semantics. It does not mutate a graph store, registry, or ontology.
