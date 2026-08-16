# S302 — M8 Temporal & Historical Query Contract

## Purpose

Define the governed read boundary for reconstructing Canonical Fact state at an explicit point or interval in time, without rewriting history or confusing historical truth with current truth.

## Temporal dimensions

- Every temporal query MUST declare its temporal basis: Effective Time, Recorded Time, or an explicitly governed combination.
- Effective Time represents when a Canonical Fact is asserted to hold in the modeled domain.
- Recorded Time represents when the governed system recorded the Fact Version or lifecycle transition.
- A query MUST NOT silently substitute Recorded Time for Effective Time, or vice versa.
- Open-ended and future-effective facts MUST have explicit temporal semantics.

## Historical reconstruction

- A historical query MUST be evaluated against the applicable Fact Version and lifecycle history rather than the current Canonical state alone.
- The result MUST be reconstructable from retained Fact Versions and append-only lifecycle transitions.
- Superseded, retired, invalidated, disputed, and deferred states MUST remain distinguishable in historical results.
- A historical query MUST NOT mutate Canonical Facts, Fact Versions, lifecycle records, provenance, evidence, or resolution history.
- Historical reconstruction MUST preserve the source identity, provenance, enterprise scope, and governing decision references attached to the applicable Fact Version.

## Current versus historical truth

- A current-state query MUST identify that it requests the presently effective governed state.
- A point-in-time query MUST identify its temporal boundary explicitly.
- A query for a past state MUST NOT be silently answered with the current Canonical Truth.
- A historical query MUST NOT be silently answered with the current Canonical Truth.
- If the requested state cannot be reconstructed, the result MUST expose that limitation rather than fabricate or silently substitute a state.

## Intervals and temporal conflicts

- Interval queries MUST define their inclusion/exclusion semantics for boundaries.
- Overlapping Fact Versions MUST remain observable when their temporal or governance semantics conflict.
- Temporal overlap MUST NOT be resolved by silently discarding one Fact Version.
- Conflicting historical assertions MUST remain linked to their conflict or resolution records.

## Replayability and provenance

- The same historical query against the same immutable Fact Version and lifecycle history MUST be replayable to the same governed result.
- Query results MUST retain sufficient references to identify the Fact Versions and lifecycle transitions used for reconstruction.
- Query execution MUST NOT rewrite historical application outcomes or resolution decisions.
- A historical result MUST be distinguishable from an inferred or projected result.

## Query outcomes

A temporal query MUST produce an explicit outcome such as `resolved`, `unresolved`, `conflicted`, `not-recorded`, or `unsupported-temporal-semantics`.

- `resolved` MUST reference the applicable Fact Version or governed set of versions.
- `unresolved` MUST remain observable and MUST NOT be promoted to Canonical Truth.
- `conflicted` MUST expose the relevant competing assertions and conflict references.
- `not-recorded` MUST indicate that the requested historical state is not present in retained history.
- `unsupported-temporal-semantics` MUST NOT be silently converted into a different temporal interpretation.

## Boundary against mutation

Temporal Query, Historical Reconstruction, Reporting, Projection, and Replay MUST remain read-only. They MUST NOT create, update, delete, supersede, invalidate, or otherwise mutate Canonical Facts or their historical records.

## Non-goals

This slice does not define a database query language, temporal database engine, indexing strategy, storage implementation, distributed consistency protocol, analytics product, authorization implementation, or automatic temporal inference. It defines the governance contract that such implementations MUST satisfy.
