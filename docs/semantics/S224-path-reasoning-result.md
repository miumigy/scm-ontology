# S224 — Path Reasoning Result

S224 defines the result contract for reasoning over existing relation paths.

```text
Path Query
   ↓
Path Constraint
   ↓
Path Evidence
   ↓
PathReasoningResult
```

A path reasoning result contains evidenced paths rather than bare node identities. This preserves the traversed relationship context and its provenance for downstream explanation.

The model is immutable and records results only; it does not infer or mutate graph state.
