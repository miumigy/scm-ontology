# S212 — Relation Instance Projection

S212 defines the read-only projection from a canonical relation instance to a graph-edge descriptor.

```text
CanonicalRelation
  ├─ relation_id
  ├─ subject_id
  ├─ predicate_ref
  ├─ object_id
  └─ qualifiers
        ↓
RelationGraphEdge
```

Identity and predicate semantics are preserved exactly. Qualifiers are copied into a detached mapping so the graph descriptor does not alias the source mapping.

This projection does not mutate a graph store, registry, or ontology.
