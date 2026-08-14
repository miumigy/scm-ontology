# S27 — Canonical SCM Relationship Contract

## Purpose

S27 promotes relationships to explicit semantic contracts. A graph edge is not merely a storage link; its predicate carries domain meaning.

## Minimal contract

```text
CanonicalRelationship
├─ source_type
├─ predicate
└─ target_type
```

## Initial canonical relationships

```text
Inventory ──for_item──→ Item
Inventory ──held_at───→ Location
Demand    ──for_item──→ Item
```

These relations make the current domain graph explicit without adding lifecycle or planning behavior.

## Rules

1. A predicate must have one stable semantic meaning.
2. Direction matters: `Inventory held_at Location` is not interchangeable with its inverse.
3. Source and target types are part of the contract.
4. A relationship must not silently encode state transitions, calculations, or business policy.
5. Synonyms are not automatically separate predicates.
6. A new relationship requires an explicit semantic definition before implementation.

## Current graph

```text
             Item
            ↑   ↑
            │   │
     for_item   │
            │   │
        Inventory ──held_at──→ Location
            ↑
            │
        for_item
            │
          Demand
```

## Non-goals

S27 does not define:

- relationship cardinality rules
- lifecycle transitions
- causal inference
- planning calculations
- temporal validity intervals
- graph database implementation details
