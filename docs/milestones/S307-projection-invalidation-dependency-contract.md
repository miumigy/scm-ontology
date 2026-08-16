# S307 — Projection Invalidation & Dependency Propagation Contract

## Purpose

Define the governed boundary for invalidating and rebuilding projections when Canonical Fact Versions, lifecycle states, provenance, conflicts, or governed configuration change.

## Dependency identity

- Every materialized or queryable projection MUST expose its dependency identity sufficiently to determine affected source state.
- Dependency records MUST reference the applicable Canonical Fact Versions, projection definition, temporal basis, and scope.
- Dependency tracking MUST remain historical and replayable.

## Invalidation semantics

- A Canonical change that makes a projection no longer valid MUST produce an explicit invalidation or rebuild-required outcome.
- Invalidation MUST identify the affected projection and the source dependency that caused the invalidation.
- `stale`, `invalid`, and `rebuild-required` states MUST remain distinguishable.
- Invalidation MUST NOT silently present an affected projection as current Canonical Truth.
- A projection that cannot establish dependency impact MUST expose an explicit unknown-impact outcome rather than assuming validity.

## Impact propagation

- Dependency propagation MUST preserve source identity and provenance.
- Partial impact MUST remain observable; unaffected projection scope MUST NOT be treated as affected without evidence.
- Cross-projection propagation MUST preserve the dependency chain needed to explain why each projection became stale or invalid.
- Propagation MUST NOT expand across enterprise, tenant, organizational, product, or other governed boundaries implicitly.

## Rebuild boundary

- Rebuild MUST use an explicit governed projection definition and identified source state.
- Rebuild MUST NOT mutate Canonical Facts, Fact Versions, lifecycle history, provenance, evidence, conflict records, or resolution records.
- A rebuild MUST create a distinguishable result and MUST NOT erase historical projection or invalidation records.
- Failed or partial rebuilds MUST remain observable.

## Conflict and resolution interaction

- A Canonical conflict, resolution, invalidation, supersession, retirement, or deferral that affects projection dependencies MUST be represented in the projection lifecycle.
- Conflict resolution MUST NOT silently restore a projection to `current`; freshness and dependency validity MUST be re-established.
- Historical projections MUST retain the dependency and resolution context under which they were produced.

## Determinism and replay

- Given the same dependency graph, Canonical Fact Versions, projection definition, temporal basis, scope, and governed configuration, invalidation impact determination MUST be deterministic unless nondeterminism is explicitly declared.
- Invalidation and rebuild decisions MUST be replayable.
- Replay MUST NOT rewrite historical Canonical or projection records.

## Explicit outcomes

Dependency evaluation MUST expose an explicit outcome such as `valid`, `stale`, `invalid`, `rebuild-required`, `unknown-impact`, `partial`, or `failed` when applicable.

- `valid` MUST be supported by current dependency evidence.
- `stale` MUST identify the source change requiring refresh.
- `invalid` MUST identify the dependency or semantic condition that invalidated the projection.
- `rebuild-required` MUST NOT be represented as merely stale when a rebuild is semantically required.
- `unknown-impact` MUST remain observable.

## Mutation boundary

Projection invalidation, dependency propagation, impact analysis, rebuild planning, and replay MUST remain read-only with respect to Canonical Truth. Any Canonical mutation MUST occur only through an explicit governed application step.

## Non-goals

This slice does not define a scheduler, graph database implementation, event bus, cache engine, distributed invalidation protocol, authorization service, or automatic Canonical mutation mechanism. It defines the governance contract such implementations MUST satisfy.
