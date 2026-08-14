# S118 — Validation / Consistency Rules

S118 adds semantic validation above the structural JSON Schema introduced in S116.

## Validation layers

```text
S116 Structural Schema
        ↓
S118 Semantic Consistency
        ↓
Future domain / enterprise validation
```

S118 checks facts that a JSON Schema alone cannot safely express:

- relationship endpoints reference declared concepts;
- concepts are uniquely declared;
- relationship signatures are not duplicated;
- identity attributes use identifier/reference semantics;
- measure attributes do not collapse into arbitrary scalar flags.

## Boundary

S118 does **not** infer business truth. It does not decide whether a planning policy is good, whether a KPI target is appropriate, or whether an enterprise mapping is semantically correct.

It also does not collapse:

- planned into actual;
- observed into inferred;
- prediction into fact;
- recommendation into decision.

Those distinctions remain explicit semantic contracts.

## Diagnostics

Validation returns structured `ValidationIssue` values with a stable `code`, human-readable `message`, and semantic `path`. This allows future CI, editors, loaders, and Graph validators to consume diagnostics without parsing prose.

## Exit criteria

S118 establishes the first semantic validation layer. More exhaustive temporal, provenance, identifier-resolution, causal, and cross-document invariants can be added in later validation milestones without changing the canonical model.
