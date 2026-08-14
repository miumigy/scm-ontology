# S48 — Cross-entity Semantic Validation

## Purpose

S48 extends S47 relationship-level validation to a minimal semantic graph context. It validates consistency that cannot be established from one relationship alone.

## Canonical scope

S48 introduces two minimal contextual primitives:

```text
SemanticNode
├─ node_id
└─ node_type

SemanticGraph
├─ nodes
└─ relationships
```

These are validation context primitives, not a database schema or a final graph serialization model.

## Initial validation rules

### 1. Endpoint resolution

A relationship endpoint should resolve to a node in the supplied graph context.

```text
R1: Order-1 ──places──→ Customer-1

nodes:
  Order-1    ✓
  Customer-1 ✓
```

If an endpoint is absent, S48 emits `UNRESOLVED_ENDPOINT / WARNING`.

A warning is intentional: a graph may be a partial view of a larger enterprise semantic graph.

### 2. Entity type consistency

A single node identifier must not be assigned conflicting semantic types within the same validation context.

```text
Order-1 → CustomerOrder
Order-1 → Shipment
```

produces `ENTITY_TYPE_CONFLICT / ERROR`.

This is a cross-entity consistency rule, not a restriction on what entity types the ontology may contain.

### 3. Relationship identity consistency

A `relationship_id` may identify only one `RelationshipInstance` within the supplied graph context.

```text
R1 = Order-1 ──places──→ Customer-1
R1 = Order-2 ──places──→ Customer-1
```

produces `RELATIONSHIP_IDENTITY_CONFLICT / ERROR`.

This operationalizes the S45 first-class identity contract at graph scope without changing S45.

## Open-world boundary

S48 does not reject domain-specific predicates. A relationship with an unknown predicate remains outside the canonical vocabulary but is not rejected merely for that reason.

S48 also does not require every possible entity in an enterprise to be present in the supplied graph.

## Severity

```text
ERROR   = cross-entity semantic contradiction
WARNING = unresolved reference in a potentially partial graph
INFO    = informational finding
```

## Explicit non-goals

S48 does not define:

- a persistent graph database model
- RDF / OWL / SHACL
- JSON-LD serialization
- graph storage or indexing
- entity lifecycle semantics
- global identity management
- inference across arbitrary predicates
- temporal graph reasoning
- automatic repair
- a closed-world entity registry

These remain implementation or later semantic-contract concerns.
