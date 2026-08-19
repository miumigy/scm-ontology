# S312 — Graph Store Adapter

S312 turns the S311 persistence plan into an executable storage boundary without binding the ontology to a graph database.

```text
CanonicalGraph
    -> S311 PersistencePlan
    -> GraphStoreAdapter
    -> applied / replayed
```

## Reference implementation

`InMemoryGraphStore` is the reference adapter for tests and integration development. A production adapter may target Neo4j, RDF, SQL, or another store, provided it preserves the same contract.

## Required checks

1. Only `planned` persistence intents may be applied.
2. The supplied graph must hash to the `PersistencePlan.graph_digest`.
3. The `plan_id` is an idempotency key.
4. Replaying the same plan returns `replayed=true` and does not create another stored graph.
5. Reusing a plan ID with a different graph is rejected.
6. Rejected or unauthorized plans never reach the adapter's storage path.

## Truth boundary

The adapter persists a `CanonicalGraph` representation. It does not perform mapping, identity resolution, inference, conflict resolution, or governed Canonical Fact application.

Storage success means **graph-store persistence succeeded**. It does not by itself authorize, validate, or promote source evidence into Canonical Truth.

## Next

Implement a concrete Neo4j adapter behind `GraphStoreAdapter`, with explicit transaction handling and preservation of the same digest/idempotency semantics. Keep the Neo4j dependency outside the semantic core.
