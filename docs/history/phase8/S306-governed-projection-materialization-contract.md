# S306 — Governed Projection Materialization Contract

## Purpose

Define the governance boundary for materializing derived projections while preserving Canonical Truth, source lineage, temporal semantics, freshness, lifecycle history, and explicit uncertainty.

## Materialization identity

- Every materialized projection MUST identify its projection definition, source state, and materialization version.
- Materialization metadata MUST retain source Fact Versions or governed graph state sufficient to reconstruct lineage.
- A materialized projection MUST remain distinguishable from Canonical Truth.

## Freshness and refresh

- Every materialized projection MUST expose a freshness state.
- Refresh MUST establish which source state was used and when the materialization was produced.
- A failed or partial refresh MUST remain observable and MUST NOT be represented as a successful current materialization.
- Refresh MUST NOT silently change temporal basis, scope, or projection definition.
- Stale materializations MUST remain explicitly stale until a governed refresh establishes otherwise.

## Historical preservation

- A new materialization MUST NOT overwrite historical materialization lineage.
- Historical materialization records MUST remain reconstructable from retained source and projection metadata.
- Materialization refresh MUST NOT rewrite Canonical Facts, Fact Versions, lifecycle transitions, provenance, evidence, conflicts, or resolution history.

## Determinism and replay

- Materialization MUST be deterministic for the same immutable source state, projection definition, temporal basis, scope, and governed configuration unless nondeterminism is explicitly declared.
- Materialization MUST be replayable.
- Replay MUST produce a distinguishable materialization result without mutating Canonical Truth or historical records.

## Failure and uncertainty

- `current`, `stale`, `partial`, `failed`, `conflicted`, `unresolved`, and `unsupported` materialization outcomes MUST remain distinguishable where applicable.
- Partial materialization MUST identify its incomplete state or affected scope.
- Conflicted or unresolved source state MUST NOT be silently promoted into an unqualified Canonical result.
- An unavailable source state MUST NOT be silently replaced with a different source state.

## Mutation boundary

Materialization, refresh, rebuild, and replay MUST NOT create, update, delete, supersede, invalidate, or otherwise mutate Canonical Facts or their historical records. Any governed Canonical mutation MUST occur through an explicit application step outside the materialization boundary.

## Scope isolation

- Materialization scope MUST be explicit.
- A refresh or rebuild MUST NOT implicitly expand across enterprise, tenant, organization, product, or other governed boundaries.
- Cross-scope materialization MUST preserve constituent source identity and lineage.

## Non-goals

This slice does not define a database engine, cache technology, scheduler, distributed consistency protocol, storage format, query language, authorization implementation, or production orchestration. It defines the governance contract that materialization implementations MUST satisfy.
