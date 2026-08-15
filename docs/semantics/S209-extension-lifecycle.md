# S209 — Extension Lifecycle

S209 defines the governed lifecycle of an ontology extension.

```text
PROPOSED
   ├─ ACCEPTED → APPLIED → DEPRECATED
   │                 └────→ ROLLED_BACK → DEPRECATED
   └─ REJECTED
```

The lifecycle prevents an extension from bypassing governance by transitioning directly from proposed to applied. State transitions are immutable and do not mutate the registry or graph.
