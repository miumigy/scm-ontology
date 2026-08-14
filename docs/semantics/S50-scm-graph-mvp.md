# S50 — SCM Graph MVP

## Semantic Contract

S50 defines a minimal execution layer over the canonical graph representation established by S49. It provides an in-memory graph facade for adding canonical nodes and relationships, resolving objects by identity, and traversing relationships.

## Canonical Boundary

```text
SCM Ontology
    ↓
Canonical Semantic Model
    ↓
CanonicalGraph
    ↓
SCMGraph (execution layer)
```

`SCMGraph` is not a database schema, persistence model, graph database API, or alternative ontology. The canonical model remains the source of semantic meaning.

## Minimum Operations

- add a node with unique `node_id`
- add a relationship with unique `relationship_id`
- require relationship endpoints to resolve to existing nodes
- retrieve nodes and relationships by identity
- traverse adjacent nodes by direction and predicate
- retrieve outgoing/incoming relationships
- return the underlying `CanonicalGraph`
- preserve deterministic S49 JSON serialization

## Identity

S45 `relationship_id` remains the identity of a relationship. S46 versions and validity remain attached to the canonical relationship and are not reinterpreted by the graph engine.

## Deliberate Non-goals

S50 does not define graph database persistence, indexing strategy, distributed graph execution, query language, inference or reasoning, temporal graph algebra, RDF/OWL/SHACL semantics, global identity management, authorization, or multi-tenancy.

## Validation Boundary

S50 enforces only graph-structural invariants required to construct an executable graph, such as unique identities and resolvable endpoints. S47/S48 semantic validation remains a separate concern and can be applied to the canonical graph without making the graph engine itself the ontology linter.
