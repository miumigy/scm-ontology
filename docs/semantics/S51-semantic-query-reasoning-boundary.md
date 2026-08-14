# S51 — Semantic Query / Reasoning Boundary

## Semantic Contract

S51 defines a minimal read-only semantic query layer over the S50 SCM Graph.
It retrieves facts explicitly represented in the canonical graph. It does not infer new facts.

```text
Canonical Graph
      ↓
Semantic Query
      ↓
Explicit graph facts
      ↓
[future] Reasoning
```

## Query Scope

S51 supports:

- node retrieval filtered by `node_type`
- relationship retrieval filtered by predicate and endpoints
- neighbor traversal by direction and predicate
- a simple fact count for graph inspection

## Reasoning Boundary

A query result is a fact represented by the graph. A derived conclusion is not a query result merely because it can be reached by traversal.

For example, traversing `Order -> supplied_by -> Supplier` retrieves an explicit relationship. Concluding that a Supplier is capable of supplying an Order is future reasoning and is outside S51.

## Canonical Boundary

`SemanticQuery` is an execution/read facade. It does not define a new ontology, query language, inference rule set, persistence model, or graph database API.

## Deliberate Non-goals

- inference or rule execution
- path algebra
- SPARQL or other query-language compatibility
- temporal reasoning
- probabilistic reasoning
- domain-specific SCM rules
- mutation through the query facade
- persistence or indexing
