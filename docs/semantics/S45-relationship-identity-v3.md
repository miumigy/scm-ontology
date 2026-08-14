# S45 — Relationship Identity Contract

A relationship is a first-class semantic object with a stable identity independent of qualifiers.

```text
RelationshipInstance
├─ relationship_id
├─ from_id
├─ predicate
└─ to_id
```

This enables distinct relationship instances to share a predicate and allows qualifiers to change without inherently changing identity.
