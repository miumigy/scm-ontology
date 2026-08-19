# S340 — Context Assembly Boundary

S340 defines the boundary for assembling explicit observations into the existing S333 `DecisionContext`.

```text
Graph Observation / other observation producers
                    ↓
          S340 Context Assembly
                    ↓
          S333 DecisionContext
                    ↓
          Decision Proposal / Reasoning
```

## Contract

`assemble_decision_context(context_id, observations)` delegates semantic
invariants to the canonical S333 context builder.

- observations remain explicit and immutable;
- `question_id` must be unique within a context;
- observation ordering is deterministic by `question_id`;
- evidence and provenance remain attached to each observation;
- blank context identifiers fail closed;
- no observation is silently overwritten or merged;
- no reasoning, inference, graph mutation, or new ontology entity is introduced.

S340 is therefore an assembly boundary, not a second DecisionContext model.
