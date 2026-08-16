# S305 — Governed Projection Query Contract

## Purpose

Define the governed read contract for querying derived projections while preserving Canonical Truth boundaries, lineage, temporal semantics, freshness, scope, and explicit uncertainty.

## Query identity

- Every projection query MUST identify the projection definition or governed view being queried.
- Query parameters MUST make temporal basis, scope, and freshness requirements explicit where applicable.
- A projection query MUST NOT silently reinterpret missing parameters into a different temporal or scope semantics.

## Canonical boundary

- Projection query results MUST remain distinguishable from Canonical Truth.
- A projection query MUST NOT create, update, delete, supersede, invalidate, or otherwise mutate Canonical Facts or Fact Versions.
- Query execution MUST NOT alter provenance, evidence, conflict records, resolution records, or historical lineage.
- A projection result MUST preserve references to its source lineage sufficient to explain how the result was derived.

## Freshness and temporal semantics

- A query requesting current data MUST define what `current` means for the projection and its source state.
- A freshness-constrained query MUST expose whether the projection satisfies the requested freshness condition.
- A stale or unknown-freshness projection MUST NOT be silently returned as current Canonical Truth.
- Historical or point-in-time projection queries MUST preserve the requested Effective Time or Recorded Time semantics.
- Temporal ambiguity MUST remain observable rather than being silently resolved.

## Scope and security boundary

- Query scope MUST remain explicit and MUST NOT expand implicitly across enterprises, tenants, organizations, or other governed boundaries.
- Aggregation across scopes MUST preserve sufficient lineage to explain constituent source states.
- Authorization is outside this contract, but implementations MUST NOT treat projection semantics as an authorization decision.

## Uncertainty and conflicts

- Conflicted, unresolved, stale, unavailable, and unsupported results MUST remain observable through explicit outcomes or metadata.
- A query MUST NOT silently discard conflicting source states when they materially affect the result.
- An unresolved result MUST NOT be promoted to Canonical Truth by the query layer.
- If a requested projection cannot be reconstructed or refreshed to the required state, the query MUST expose that limitation.

## Determinism and replay

- The same query against the same immutable projection state, definition, temporal basis, scope, and governed configuration MUST return the same governed result unless nondeterminism is explicitly declared.
- Query execution MUST be replayable from retained projection and lineage state.
- Replaying a query MUST NOT rewrite historical query results or projection lineage.

## Explicit outcomes

A projection query MUST expose an explicit outcome such as `resolved`, `stale`, `unknown-freshness`, `conflicted`, `unresolved`, `not-available`, or `unsupported` when applicable.

- `resolved` MUST retain the projection lineage used for the result.
- `stale` MUST expose the freshness condition that was not satisfied.
- `conflicted` and `unresolved` MUST remain observable.
- `not-available` MUST distinguish unavailable projection state from an empty valid result.
- `unsupported` MUST NOT be silently converted into a different query interpretation.

## Non-goals

This slice does not define a query language, authorization implementation, graph database engine, cache implementation, materialized-view engine, transport API, or UI. It defines the governance contract that projection query implementations MUST satisfy.
