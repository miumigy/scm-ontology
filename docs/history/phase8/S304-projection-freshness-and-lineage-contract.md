# S304 — Projection Freshness & Lineage Contract

## Purpose

Define the governance boundary for derived projections of Canonical Graph state, including freshness, lineage, temporal basis, and invalidation semantics.

## Projection identity and lineage

- Every projection MUST identify the Canonical Fact Versions or governed graph state from which it was derived.
- Projection lineage MUST remain traceable to source Fact Versions, provenance, temporal basis, scope, and applicable lifecycle state.
- A projection MUST NOT be presented as Canonical Truth merely because it is derived from Canonical data.
- Projection lineage MUST be replayable from retained source state and the governed projection definition.

## Freshness

- Every projection MUST expose a freshness state or sufficient metadata to determine freshness.
- Freshness MUST be evaluated against an explicit source version, recorded time, effective time, or governed combination.
- A stale projection MUST remain observable as stale.
- A consumer MUST NOT silently treat a stale projection as current Canonical Truth.
- If freshness cannot be established, the projection MUST expose an explicit unknown or unsupported freshness outcome.

## Temporal and scope semantics

- A projection MUST preserve the temporal basis of the source state.
- A projection MUST NOT silently mix Effective Time and Recorded Time semantics.
- Projection scope MUST remain explicit, including enterprise, tenant, organizational, and other governed boundaries where applicable.
- Cross-scope aggregation MUST preserve the identity and provenance context necessary to explain the resulting projection.

## Conflicts and lifecycle

- Conflicting source Fact Versions MUST remain observable in a projection where they affect the represented result.
- Unresolved, disputed, invalidated, deferred, retired, and superseded source states MUST NOT be silently converted into an unqualified current state.
- Projection logic MUST preserve references to applicable conflict and resolution records when they materially affect the result.

## Determinism and replay

- Given the same immutable source Fact Versions, projection definition, temporal basis, scope, and governed configuration, projection generation MUST be deterministic or explicitly expose nondeterminism.
- Projection generation MUST be replayable.
- Replaying a projection MUST NOT mutate Canonical Facts, Fact Versions, lifecycle history, provenance, evidence, or resolution records.
- Projection refresh MUST NOT rewrite historical projection lineage; a new projection result MUST be distinguishable from prior results.

## Mutation boundary

Canonical Graph Read, Projection Generation, Projection Refresh, and Projection Replay MUST remain read-only with respect to Canonical Truth. They MUST NOT create, update, delete, supersede, invalidate, or otherwise mutate Canonical Facts or their historical records.

## Explicit outcomes

A projection MUST expose an explicit outcome such as `current`, `stale`, `unknown-freshness`, `conflicted`, `unresolved`, or `unsupported` when applicable.

- `current` MUST identify the source state used to establish freshness.
- `stale` MUST identify or reference the source state against which staleness was determined.
- `conflicted` and `unresolved` MUST remain observable and MUST NOT be promoted to Canonical Truth.
- `unsupported` MUST NOT be silently converted into a different projection interpretation.

## Non-goals

This slice does not define a graph database implementation, query language, indexing strategy, materialized-view engine, cache implementation, authorization service, distributed consistency protocol, or analytics product. It defines the governance contract that such implementations MUST satisfy.
