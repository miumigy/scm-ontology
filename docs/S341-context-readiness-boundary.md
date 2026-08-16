# S341 — Decision Context Readiness Boundary

S341 defines the fail-closed boundary between an assembled `DecisionContext` and downstream reasoning.

```text
DecisionContext (S333)
        ↓
Readiness Validation (S341)
        ↓
Decision-ready Context
```

## Readiness requirements

A context is ready only when:

- it contains at least one observation;
- every observation has at least one evidence identifier; and
- every observation has at least one provenance identifier.

The existing S333 contract remains authoritative for `context_id`, unique `question_id`, and deterministic ordering.

## Scope

S341 validates governance completeness only. It does not infer business meaning, mutate observations, create decisions, resolve identities, or access a graph store.

`require_context_ready()` fails closed and returns the original immutable context only when all readiness requirements are satisfied.
