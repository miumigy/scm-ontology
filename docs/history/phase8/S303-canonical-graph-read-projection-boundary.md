# S303 — M8 Canonical Graph Read & Projection Boundary

## Purpose

Define the governed read boundary for accessing Canonical Graph state and producing read-only projections without confusing a projection or derived view with Canonical Truth.

## Canonical graph reads

- A Canonical Graph read MUST identify the applicable enterprise scope, temporal basis, and Fact Version context.
- A read result MUST preserve references to source identity, provenance, evidence, and governing decisions where applicable.
- Current-state reads MUST distinguish presently governed Canonical Truth from historical or projected state.
- Historical reads MUST follow the S302 temporal and historical query contract.
- Conflicts, unresolved identity, disputed facts, and other non-canonical outcomes MUST remain observable in read results.

## Projection boundary

- A projection is a derived read representation and MUST NOT be represented as Canonical Truth merely because it was produced from Canonical Graph data.
- Projection logic MUST be read-only with respect to the Canonical Ontology and Canonical Facts.
- A projection MUST retain sufficient lineage to identify the Canonical Fact Versions and query context from which it was derived.
- Derived calculations, aggregations, rankings, classifications, and convenience representations MUST remain distinguishable from source Canonical Facts.
- A projection MUST NOT silently create, update, delete, supersede, invalidate, or rewrite Canonical Facts.

## Semantic fidelity

- A graph read MUST NOT silently omit provenance, conflicts, unresolved outcomes, or lifecycle state when those elements are required to interpret the result.
- Transformations that change semantic meaning MUST be explicitly identified as derived or projected semantics.
- Projection rules MUST NOT introduce vendor-specific semantics into the Canonical Ontology.
- A projection MUST NOT infer Canonical Truth from aggregation, similarity, ranking, or successful transformation alone.

## Replayability and freshness

- The same projection against the same immutable Canonical Fact Versions and query context MUST be replayable to the same governed result.
- A projection MUST expose its source version or snapshot context sufficiently to determine freshness.
- Stale projections MUST be identifiable and MUST NOT silently masquerade as current Canonical Truth.
- If source state required for a projection is unavailable, the projection MUST expose that limitation rather than fabricate or silently substitute data.

## Scope and authorization boundary

- Graph reads MUST respect the explicitly governed enterprise, tenant, and data scope of the request.
- A projection MUST NOT broaden the scope of the underlying Canonical Graph read implicitly.
- Authorization and access-control decisions MUST remain explicit governance inputs; successful projection execution MUST NOT itself authorize broader access.

## Outcomes

A governed graph read or projection MUST expose an explicit outcome such as `resolved`, `partial`, `conflicted`, `unresolved`, `stale`, `not-found`, or `unsupported`.

- `resolved` MUST identify the applicable source Fact Version or governed source set.
- `partial` MUST identify what source information is unavailable or omitted.
- `conflicted` MUST preserve references to the competing assertions or conflict records.
- `unresolved` MUST remain distinguishable from Canonical Truth.
- `stale` MUST identify the relevant freshness/version context.
- `not-found` MUST NOT be converted into an inferred Canonical entity or fact.
- `unsupported` MUST NOT be silently converted into another query or projection interpretation.

## Boundary against mutation

Canonical Graph Read, Historical Reconstruction, Projection, Reporting, and Replay MUST remain read-only. They MUST NOT mutate Canonical Facts, Fact Versions, provenance, evidence, conflict records, resolution records, or the Canonical Ontology.

## Non-goals

This slice does not define a graph database implementation, query language, indexing strategy, materialized-view engine, cache implementation, authorization service, analytics product, distributed consistency protocol, or vendor connector. It defines the governance contract that such implementations MUST satisfy.
