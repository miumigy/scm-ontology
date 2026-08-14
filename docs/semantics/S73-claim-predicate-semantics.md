# S73 — Claim Predicate Semantics

S73 defines `Claim.predicate` as using the same canonical predicate semantics as Relationship predicates defined by S41. Claim and Relationship remain distinct semantic objects.

## Canonical decision

```text
Canonical Predicate Vocabulary
          │
          ├── Relationship → predicate
          └── Claim        → predicate
```

The vocabulary is reusable but remains open. Domain-specific predicates are permitted; unknown predicates are not rejected merely because they are absent from the current canonical vocabulary.

Examples of canonical predicates include `contains`, `located_at`, `part_of`, `plays_role`, `places`, `receives`, `executes`, `establishes`, `changes`, `moves_to`, `supplies`, and `consumes`.

## Claim examples

A relationship-valued claim can use the same predicate semantics as a graph relationship:

```text
Order-001 → supplied_by → Supplier-A
```

A value-valued claim can use a predicate with the same canonical semantic role:

```text
Shipment-001 → has_status → "delivered"
```

The predicate does not determine whether the object is a reference or literal; S71 Claim Object Semantics defines that distinction.

## Boundaries

```text
Claim ≠ Relationship
Claim predicate = Canonical predicate semantics
Predicate ≠ endpoint constraint ≠ cardinality ≠ relationship identity ≠ qualifier ≠ validity
```

S42 endpoint constraints, S43 cardinality, S44 qualifiers, S45 identity, and S46 validity remain Relationship-specific contracts unless separately applied by a later contract.

Source-system predicates may be normalized through Semantic Mapping, for example `SUPPLIES_TO → supplies`. S73 does not define an automatic synonym registry or mapping algorithm.

## Non-goals

S73 does not define a closed predicate enum, RDF/OWL semantics, inverse generation, automatic synonym resolution, Claim endpoint validation, automatic Claim-to-Relationship conversion, or graph serialization.
