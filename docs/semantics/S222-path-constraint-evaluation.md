# S222 — Path Constraint Evaluation

S222 evaluates explicit constraints against paths that already exist in the canonical graph.

Initial constraint:

```text
PathEndsAt(node_id)
```

```text
RelationPathQuery
      ↓
existing RelationPathMatch*
      ↓
PathEndsAt
      ↓
matching paths
```

No new edge or inferred path is created. The evaluator only filters paths produced by S221.
