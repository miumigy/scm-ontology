# S227 — Reasoning Explanation

S227 defines a deterministic, machine-readable explanation trace derived from an existing reasoning result.

```text
PathReasoningResult
       ↓
ReasoningExplanation
       ├─ relationship steps
       └─ evidence steps
```

Explanation is derived from existing canonical identities and provenance. It does not create facts, infer relationships, assign confidence, or mutate graph state.

An empty result remains explainable through an explicit result-status step.
