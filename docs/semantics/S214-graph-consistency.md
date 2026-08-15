# S214 — Graph Consistency

S214 defines the minimum structural consistency invariant for the canonical graph.

Every relationship endpoint must resolve to an existing graph node.

```text
Node Registry
    ↑      ↑
    │      │
 relationship.from / relationship.to
```

Dangling relationship endpoints are rejected before downstream reasoning consumes the graph.

The validator is read-only and does not repair, delete, or mutate graph state.
