# S313 — Optional Neo4j Graph Store Adapter

S313 proves that the governed S311/S312 persistence contracts can reach a concrete graph transport without introducing a database dependency into the semantic core.

## Boundary

```text
CanonicalGraph
  -> S311 PersistencePlan
  -> S312 GraphStoreAdapter contract
  -> S313 Neo4jGraphStoreAdapter
  -> injected transaction callable
```

The adapter receives an already-authorized `PersistencePlan`. It rejects any non-`planned` intent and passes only the canonical graph node payload to the injected transport callable.

No Neo4j driver is imported by the ontology package. The application layer owns driver/session/transaction lifecycle.

## Deliberate limitations

This first adapter slice writes canonical nodes only. Relationship persistence, transaction semantics, retries, and production connection management are subsequent application-layer concerns. No identity resolution or Canonical Truth promotion is introduced.
