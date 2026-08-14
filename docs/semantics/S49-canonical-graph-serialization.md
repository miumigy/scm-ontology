# S49 — Canonical Graph Representation and Serialization

## Purpose

S49 defines the minimum machine-readable representation of a canonical SCM graph.
It is a semantic graph contract first and a serialization contract second.

The contract allows a canonical graph to be exchanged as a JSON document without making JSON, RDF/OWL, SHACL, or a graph database the ontology itself.

## Canonical model

```text
CanonicalGraph
├─ nodes
│  └─ SemanticNode
│     ├─ id
│     ├─ type
│     └─ properties (optional)
│
└─ relationships
   └─ CanonicalRelationship
      ├─ id
      ├─ from
      ├─ predicate
      ├─ to
      └─ versions (optional)
         └─ RelationshipVersion
            ├─ valid_from
            ├─ valid_to
            └─ qualifiers (optional)
```

## Identity

`node.id` is the stable semantic identity of a node within the canonical graph.

`relationship.id` is the S45 `relationship_id`. It identifies the RelationshipInstance and does not change merely because its version or qualifiers change.

Node and relationship IDs must be unique within one canonical graph document.

## Entity type and predicate

`type` carries the canonical or mapped semantic entity type.

`predicate` carries the relationship vocabulary term. Unknown or domain-specific predicates are not rejected by this representation; vocabulary validation remains the responsibility of the semantic validation layer.

## Versions and validity

A relationship may contain zero or more S46 `RelationshipVersion` values. Each version carries `valid_from`, optional `valid_to`, and optional qualifiers.

S49 does not define interval arithmetic, overlap rules, version generation, audit history, or persistence semantics.

## Properties

Properties are optional semantic attributes and qualifiers. S49 does not define a database column model, datatype registry, or enterprise-specific property schema.

## Serialization

The reference implementation provides deterministic JSON serialization using the canonical mapping. JSON is an interchange representation, not the ontology.

Serialization uses:

- UTF-8-compatible Unicode output
- deterministic key ordering
- compact JSON separators
- explicit `null` for open-ended `valid_to`

The implementation does not require consumers to use JSON internally.

## Explicit non-goals

S49 does not define:

- RDF / OWL
- SHACL
- JSON-LD
- graph database schemas
- Cypher or SQL
- persistence
- graph inference
- temporal graph reasoning
- global identity management
- closed-world entity registries

These may be mappings or implementation layers built above the canonical contract.

## Design boundary

```text
SCM Ontology
    ↓
Canonical Graph Model
    ↓
Serialization (JSON, RDF, database mapping, ...)
```

The serialization layer must not redefine canonical semantics.
