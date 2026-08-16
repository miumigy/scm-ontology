# S308 — Cross-Projection Consistency & Rebuild Boundary Contract

## Purpose

Define the governance boundary for comparing, invalidating, rebuilding, and reconciling projections that depend on overlapping Canonical Facts without weakening Canonical Truth or historical lineage.

## Consistency identity

- Every projection MUST expose its projection definition, dependency identity, temporal basis, scope, and materialization version.
- Cross-projection comparison MUST compare equivalent definitions, source state, temporal basis, and scope before declaring consistency.
- Different projection definitions MUST NOT be treated as inconsistent merely because their values differ.
- Consistency results MUST remain traceable to the compared projection versions and dependency state.

## Explicit outcomes

Consistency evaluation MUST distinguish `consistent`, `inconsistent`, `stale`, `invalid`, `rebuild-required`, `unknown`, `partial`, and `failed` outcomes where applicable.

- `unknown` MUST NOT be promoted to `consistent` by absence of detected differences.
- `partial` MUST identify the incomplete comparison or affected scope.
- `failed` MUST remain observable and MUST NOT be represented as a successful consistency result.

## Rebuild boundary

- A consistency failure MUST produce an explicit governed rebuild or investigation outcome.
- Rebuild planning MUST remain separate from Canonical mutation.
- Rebuild MUST use an explicit source Fact Version, projection definition, temporal basis, scope, and dependency snapshot.
- Rebuild MUST NOT silently broaden scope or change projection semantics.
- Rebuild MUST create a distinguishable materialization result and preserve the prior result and lineage.
- Failed, partial, or conflicting rebuilds MUST remain observable.

## Cross-projection reconciliation

- Reconciliation MUST preserve the identity and provenance of every compared projection.
- A projection discrepancy MUST NOT by itself establish which projection is Canonical Truth.
- Reconciliation MUST NOT silently overwrite one projection with another.
- Conflicting projection results MUST remain observable until a governed decision establishes the appropriate outcome.
- Resolution of a projection discrepancy MUST NOT rewrite historical projection or Canonical records.

## Dependency and temporal integrity

- Cross-projection consistency MUST respect dependency lineage and Fact Version history.
- Projections based on different Fact Versions MUST remain distinguishable even when their values happen to match.
- Historical consistency queries MUST evaluate the applicable historical projection versions rather than silently using current projections.
- Dependency changes MUST invalidate or require rebuild of affected projections according to the explicit dependency boundary.

## Mutation boundary

Cross-projection comparison, consistency evaluation, reconciliation planning, invalidation analysis, rebuild planning, and replay MUST remain read-only. Any Canonical mutation MUST occur only through an explicit governed application step.

## Replayability

- Consistency evaluation MUST be replayable from retained projection, dependency, and Fact Version records.
- Rebuild planning and execution MUST preserve historical records.
- Replaying a consistency evaluation MUST NOT silently rewrite prior outcomes.

## Scope isolation

Cross-projection operations MUST NOT expand across enterprise, tenant, organization, product, or other governed boundaries implicitly. Any cross-scope operation requires explicit governed scope.

## Non-goals

This slice does not define a database engine, distributed transaction protocol, cache implementation, scheduler, authorization system, automatic reconciliation algorithm, or production orchestration. It defines the governance contract those implementations MUST satisfy.
