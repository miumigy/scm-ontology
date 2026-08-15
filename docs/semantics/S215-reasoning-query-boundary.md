# S215 — Reasoning Query Boundary

S215 defines the first explicit read-only query boundary between the canonical graph and downstream reasoning consumers.

```text
CanonicalGraph
     ↓
Consistency Gate
     ↓
NodeQuery
     ↓
SemanticNode*
```

Queries must declare at least one constraint: canonical node type or canonical node identity. The boundary performs selection only; it does not infer new facts or mutate graph state.
