# S342 — Reasoning Input Boundary

S342 creates an immutable, storage-neutral input contract between a ready `DecisionContext` and any downstream reasoning engine.

## Boundary

```text
DecisionContext (S333)
        ↓
Context Readiness (S341)
        ↓
ReasoningInput (S342)
        ↓
Rule / LLM / Solver / Simulation / Human reasoning
```

`build_reasoning_input()` always calls the S341 fail-closed readiness gate first.

## Contract

- `context_id` identifies the source context;
- observations are carried without semantic inference;
- evidence IDs and provenance IDs are canonicalized as sorted unique tuples;
- serialization uses contract version `S342.1`;
- no reasoning, inference, mutation, identity resolution, or storage dependency is introduced.

The reasoning engine is deliberately outside the Canonical Semantic Model boundary.
