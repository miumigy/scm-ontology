# S327 — Canonical Demand/Supply Gap Business Question

## Purpose

S327 is the second Phase 4 SCM business-question vertical slice. It resolves a
demand/supply gap from already-canonical demand and supply facts while
preserving explicit evidence and provenance references.

## Contract

For each explicit `(item_id, unit, period_start, period_end)` scope:

`gap = max(demand - supply, 0)`

Missing demand or supply sides are zero. Multiple records are aggregated only
when the canonical item, unit, and period keys are identical.

The runtime emits `contract_version: S327.1` and deterministic JSON.

## Semantic boundary

S327 MUST NOT:

- perform source identity resolution;
- infer or fuzzy-match item identities or periods;
- create or mutate Canonical Truth;
- allocate supply to demand;
- decide whether a gap is actionable or requires a business response;
- query or mutate a graph store;
- manufacture evidence or provenance.

Evidence and provenance IDs are caller-supplied lineage references. Their
presence does not make the runtime an evidence adjudicator. A gap is a derived
observation, not a decision.

## Why this slice

S326 established the first Phase 4 vertical slice by resolving an inventory
position from canonical inventory facts. S327 extends the same deterministic
boundary to reconcile canonical demand against canonical supply over an explicit
period. It reuses the item/period/unit scoping discipline and keeps allocation,
optimization, and execution in separate decision boundaries.

The intended progression is:

`source data -> governed canonicalization -> canonical demand/supply facts -> S327 gap -> evidence/lineage -> explainable SCM application`

## Follow-up

Future slices can extend this same boundary to supplier delay impact, multi-hop
supply risk, capacity constraints, and network disruption propagation.
Allocation, optimization, and execution remain separate decision boundaries.
