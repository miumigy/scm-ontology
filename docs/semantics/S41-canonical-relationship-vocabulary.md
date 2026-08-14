# S41 — Canonical Relationship Vocabulary v0.2

## Purpose

S41 centralizes the small set of reusable relationship predicates used by SCM Ontology contracts. The goal is to prevent vocabulary drift while keeping domain-specific relationships explicit.

## Canonical predicate categories

### Structural

```text
contains
located_at
part_of
```

These describe composition, location, and structural membership.

### Participation

```text
plays_role
places
receives
executes
```

These describe a party's contextual participation in SCM activities or transactions.

### Lifecycle

```text
establishes
changes
```

These describe semantic effects on conditions or states.

### Flow

```text
moves_to
supplies
consumes
```

These describe movement or material/supply relationships.

## Vocabulary rules

1. Predicates are directional.
2. Predicate names describe the relationship, not the implementation class.
3. Party roles remain contextual; a predicate does not make a role intrinsic to a Party.
4. Domain-specific predicates may exist, but should not duplicate a canonical predicate with equivalent semantics.
5. Synonyms should be mapped to a canonical predicate before entering the canonical graph.

## Relationship versus predicate vocabulary

```text
Relationship
├─ from
├─ predicate ──→ CanonicalPredicate
└─ to
```

S41 defines the predicate vocabulary. It does not define every valid `from → to` pair.

## Compatibility with existing graph semantics

Existing graph relationships such as `CHANGES` can remain implementation/schema-level names while mapping semantically to the canonical `changes` predicate.

Likewise, `CARRIED_BY`, `SUPPLIES_TO`, `FOR_PRODUCT_LOCATION`, and similar domain-specific relationships are not automatically replaced. S41 establishes the semantic vocabulary first; migration or normalization of existing schema names is a separate decision.

## Non-goals

S41 does not define:

- exhaustive relationship constraints
- ontology inheritance
- cardinality
- inverse predicates
- property schemas
- graph database implementation
- automatic migration of existing YAML relationships

These require later contracts.
