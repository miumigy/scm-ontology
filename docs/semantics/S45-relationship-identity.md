# S45 — Relationship Identity Contract

S45 makes a relationship a first-class, uniquely referenceable semantic object.

```text
RelationshipInstance
├─ relationship_id
├─ from_id
├─ predicate
└─ to_id
```

`relationship_id` is the stable identity of the relationship instance. Endpoint identity, predicate meaning, cardinality, and qualifiers remain separate semantic concerns.

Two edges may share a predicate while remaining distinct instances:

```text
Order-1 ──supplied_by──→ Supplier-A   [R1]
Order-1 ──supplied_by──→ Supplier-B   [R2]
```

S44 qualifiers belong to the relationship instance but do not inherently define its identity. Versioning and temporal validity remain separate contracts.

S45 does not define ID generation algorithms, persistence keys, versioning, validity, duplicate detection, or endpoint identity semantics.
