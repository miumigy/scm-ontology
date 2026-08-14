# S43 — Canonical Relationship Cardinality

## Purpose

S43 introduces a reusable cardinality primitive and a small set of selected relationship cardinality constraints.

## Cardinality primitive

```text
Cardinality
├─ minimum
└─ maximum
```

`maximum = null` means unbounded (`*`).

Canonical forms:

```text
1
0..1
0..*
1..*
```

## Selected relationship constraints

```text
plays_role   1     → 0..*
places       0..*  → 1
receives     0..*  → 1
executes     0..*  → 1
located_at   0..*  → 1
establishes  0..*  → 0..*
changes      0..*  → 0..*
```

These describe endpoint occurrence bounds for selected predicates. They are intentionally not an exhaustive ontology-wide constraint set.

## Interpretation

For a relationship:

```text
from_cardinality → to_cardinality
```

The cardinality applies to the number of related instances in the relevant direction/context. It does not by itself establish database uniqueness, referential integrity, or implementation constraints.

## Important boundary

S43 does not define:

- inverse cardinalities as separate predicates
- database constraints
- ownership
- lifecycle requirements
- conditional cardinality
- temporal cardinality
- inheritance-based cardinality
- exhaustive constraints for every canonical predicate

## Relationship semantics stack

S41–S43 now provide three increasingly precise layers:

```text
Predicate Vocabulary
        ↓
Endpoint Type Constraint
        ↓
Cardinality Constraint
```

Together these form the initial machine-checkable contract for SCM relationships while preserving extensibility and separation from implementation schema.
