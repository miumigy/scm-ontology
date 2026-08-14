# S46 — Relationship Version / Validity Contract

S46 defines the temporal semantic state of a first-class relationship instance.

## Boundary with S45

S45 answers:

> What relationship is this?

S46 answers:

> When is this relationship version valid?

The relationship identity remains stable while its semantic representation may have multiple versions.

```text
RelationshipInstance
├─ relationship_id
├─ from_id
├─ predicate
├─ to_id
└─ versions
      └─ RelationshipVersion
           ├─ valid_from
           ├─ valid_to
           └─ qualifiers
```

## Canonical semantics

`RelationshipVersion` represents a temporal semantic version of a `RelationshipInstance`. `valid_from` is the point at which the version becomes semantically applicable. `valid_to`, when present, is the point at which it ceases to be applicable. A null `valid_to` represents an open-ended validity period.

A version does not require a canonical `version_id` in S46. Version identifiers, numbering, UUID generation, persistence keys, and revision algorithms remain implementation concerns unless a later contract establishes otherwise.

## Qualifiers

Relationship qualifiers may vary by version. A qualifier is not itself relationship identity. A change in qualifier value does not imply a new relationship identity; S46 permits the changed semantic state to be represented by another version.

```text
R1
Order-1 ──supplied_by──→ Supplier-A

V1
priority = 1
valid: 2026-01-01 → 2026-06-30

V2
priority = 2
valid: 2026-07-01 → open
```

## Intentionally out of scope

S46 does not define:

- database temporal tables
- persistence or storage schema
- event sourcing
- audit logs
- UUID or version-number generation
- timezone policy
- timestamp serialization format
- interval arithmetic
- overlap/gap detection
- automatic version creation
- version diff algorithms

These are implementation or future semantic contracts.

S46 therefore defines temporal validity without turning the Canonical Semantic Model into a temporal database schema.
