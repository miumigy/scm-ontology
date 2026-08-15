# S189 — Governance Decision Application

S189 makes governance decisions explicit and immutable.

```text
PENDING
  ├─ accept() → ACCEPTED
  └─ reject() → REJECTED
```

A decision object is immutable: applying a decision returns a new object and leaves the original pending object unchanged.

Terminal decisions cannot be reapplied or reversed through this API.

This layer does not mutate the ontology, graph, or canonical relation registry. An ACCEPTED decision is only a governance outcome; ontology extension remains a later, separately governed step.
