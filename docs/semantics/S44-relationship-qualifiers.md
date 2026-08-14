# S44 — Canonical Relationship Qualifier Contract

## Purpose

S44 defines how semantic qualifiers may attach to a relationship without confusing relationship-level facts with attributes of either endpoint entity.

## Contract

```text
Relationship
├─ from
├─ predicate
├─ to
└─ qualifiers
```

A qualifier describes the relationship itself or its applicability, rather than changing the identity of the connected entities.

## Initial canonical qualifiers

```text
valid_from       → time_reference
valid_to         → time_reference
sequence         → integer
priority         → integer
allocation_ratio → decimal
```

These are reusable vocabulary candidates, not mandatory qualifiers for every relationship.

## Entity attribute vs relationship qualifier

Use an **entity attribute** when the value describes the entity independently of a specific relationship.

Use a **relationship qualifier** when the value is meaningful only in the context of a particular edge.

Example:

```text
Supplier
  priority = ?                  # potentially entity attribute

Order ──supplied_by──→ Supplier
          │
          └─ priority = 1       # relationship-specific qualifier
```

## Temporal qualifiers

`valid_from` and `valid_to` describe applicability of the relationship, not necessarily the lifecycle of either endpoint.

```text
Order ──supplied_by──→ Supplier
          │
          ├─ valid_from = T1
          └─ valid_to   = T2
```

This allows supplier relationships, sourcing assignments, lanes, allocations, and other relationships to change over time without mutating the meaning of the endpoint entities.

## Important boundary

S44 does not define:

- mandatory qualifier sets per predicate
- qualifier cardinality
- qualifier value validation beyond primitive type labels
- temporal interval arithmetic
- entity property schemas
- implementation-specific edge properties
- automatic migration of existing relationships

Those are later contracts.

## Semantic stack

```text
S41 Predicate Vocabulary
        ↓
S42 Endpoint Type Constraint
        ↓
S43 Cardinality Constraint
        ↓
S44 Relationship Qualifiers
```

This provides the foundation for a rich SCM Graph edge while preserving a clean distinction between **node semantics** and **relationship semantics**.
