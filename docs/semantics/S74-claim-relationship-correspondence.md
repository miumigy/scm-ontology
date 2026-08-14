# S74 — Claim–Relationship Semantic Correspondence

S74 defines the semantic boundary between a Claim and a Relationship when both express the same subject–predicate–object proposition.

## Canonical decision

A Claim and a Relationship **may correspond semantically**, but they are not defined as identical objects and S74 does not define an automatic conversion.

```text
Claim
  subject ─ predicate ─ object

Relationship
  from ─ predicate ─ to
```

If a Claim has a reference-valued object, for example:

```text
Order-001 → supplied_by → Supplier-A
```

its proposition can correspond to a Relationship with the same endpoints and canonical predicate.

## Correspondence, not equivalence

The correspondence is intentionally weaker than object identity or universal equivalence.

A Relationship has contracts that a Claim does not inherently have, including:

- relationship identity
- endpoint constraints
- cardinality
- qualifiers
- validity/versioning

A Claim instead represents a semantic assertion and may carry evidence and claim validity.

Therefore:

```text
Claim ≠ Relationship
Claim may correspond to Relationship
Correspondence ≠ automatic transformation
Correspondence ≠ shared identity
```

## Literal-valued Claims

A Claim whose object is a literal value does not automatically correspond to a Relationship.

```text
Shipment-001 → has_status → "delivered"
```

The shared predicate vocabulary does not imply that every Claim is a graph edge.

## Mapping boundary

A system may define a mapping such as:

```text
Enterprise assertion
        ↓
Canonical Claim
        ↓
Semantic Mapping
        ↓
Canonical Relationship
```

but the mapping rules are outside S74. In particular, S74 does not define endpoint validation, relationship identity generation, qualifier extraction, validity propagation, or graph materialization.

## Non-goals

S74 does not define Claim-to-Relationship conversion, bidirectional synchronization, identity unification, automatic inference, RDF equivalence, or graph serialization.
