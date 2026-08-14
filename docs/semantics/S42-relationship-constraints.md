# S42 — Canonical Relationship Constraints

## Purpose

S42 makes selected relationship endpoint semantics machine-checkable without migrating or replacing the existing implementation schema.

## Contract

```text
RelationshipConstraint
├─ predicate
├─ allowed_from
└─ allowed_to
```

A constraint states which canonical concept types may participate as the source and target of a predicate.

## Initial constraints

```text
places      Party / Customer                    → CustomerOrder
receives    Party / Supplier                    → PurchaseOrder
executes    Party / Carrier                     → Shipment
establishes Event                              → State
changes     Event                              → State
located_at  Item / Party / Inventory            → Location
moves_to    PhysicalFlow / Shipment             → Location
supplies    Party / PurchaseOrder / ProductionOrder → Supply
consumes    ProductionOrder / Demand / PhysicalFlow → Supply / Item
```

These are deliberately small, representative constraints rather than an exhaustive ontology.

## Validation behavior

Known canonical predicates are checked against their constraints:

```text
places(Party, CustomerOrder) ✓
places(Shipment, Party)      ✗
```

Unknown/domain-specific predicates are not rejected by S42. This preserves extensibility and prevents the canonical vocabulary from becoming an accidental closed-world schema.

## Important boundary

S42 defines endpoint constraints only. It does not define:

- cardinality
- inverse relationships
- transitivity
- inheritance
- relationship properties
- lifecycle completeness
- domain-specific custom predicates
- migration of existing YAML relationships

## Why this matters

S41 established the vocabulary. S42 adds enough structure for automated semantic validation while preserving the distinction between:

```text
Canonical semantics
        ≠
Implementation schema
```

This is the basis for a future ontology linter and graph consistency checker.
