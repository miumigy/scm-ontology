# S45 — Relationship Identity Contract

## Purpose

S45 makes a relationship a first-class, uniquely referenceable semantic object. The identity is independent of the relationship's qualifiers and endpoint cardinality.

## Contract

```text
RelationshipInstance
├─ relationship_id
├─ from_id
├─ predicate
└─ to_id
```

`relationship_id` is the stable identity of the relationship instance. `from_id`, `predicate`, and `to_id` describe its semantic endpoints and meaning.

## Why identity matters

Two relationships can share the same predicate while remaining distinct instances:

```text
Order-1 ──supplied_by──→ Supplier-A
            relationship_id = R1
            priority = 1

Order-1 ──supplied_by──→ Supplier-B
            relationship_id = R2
            priority = 2
```

The predicate alone therefore cannot identify an edge.

## Qualifier separation

S44 qualifiers belong to the relationship instance but do not define its identity:

```text
RelationshipInstance(R1)
├─ supplied_by
├─ Order-1 → Supplier-A
└─ qualifiers
   ├─ valid_from
   └─ priority
```

Changing a qualifier does not inherently create a new relationship identity. Versioning and validity semantics are separate contracts.

## Semantic stack

```text
Relationship Identity
        ↓
Predicate Vocabulary
        ↓
Endpoint Constraints
        ↓
Cardinality
        ↓
Qualifiers
```

## Non-goals

S45 does not define:

- ID generation algorithms
- UUID requirements
- persistence/database keys
- relationship versioning
- temporal validity rules
- immutable versus mutable relationships
- duplicate detection
- endpoint identity semantics

Those remain separate concerns.
