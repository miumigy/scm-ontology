# S339 — Graph Observation Boundary

S339 converts an S338 `GraphQueryResult` into the existing `DecisionObservation` contract.

## Boundary

```text
Graph Projection (S337)
        ↓
Graph Query (S338)
        ↓
Graph Observation (S339)
        ↓
DecisionContext (S333)
```

The adapter does not infer meaning, mutate graph state, resolve identities, or make decisions.

## Contract

`graph_query_to_observation(result, question_id, query_id)`:

- requires non-empty `question_id` and `query_id`;
- embeds the deterministic S338 mapping as the observation value;
- carries query identity explicitly;
- carries projected node identifiers as evidence identifiers;
- preserves S338 provenance identifiers.

The output is the existing `DecisionObservation`, not a new ontology entity.
