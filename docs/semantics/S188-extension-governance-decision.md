# S188 — Extension Governance Decision

S188 introduces an explicit governance state for extension candidates.

```text
EXTENSION_CANDIDATE
        ↓
PENDING
        ↓
[future human/governance decision]
 ├─ ACCEPT
 └─ REJECT
```

The initial projection is always `PENDING`. This step does not approve candidates, mutate the ontology, infer new relations, or modify the graph.
