# S326 — Canonical Inventory Position Business Question

## Purpose

S326 is the first Phase 4 SCM business-question vertical slice. It resolves an
inventory position from already-canonical inventory facts while preserving
explicit evidence and provenance references.

## Contract

For each explicit `(product_id, location_id, unit)` scope:

`available = on_hand + inbound - outbound`

Missing quantity classes are zero. Multiple records are aggregated only when
the canonical product, location, and unit keys are identical.

The runtime emits `contract_version: S326.1` and deterministic JSON.

## Semantic boundary

S326 MUST NOT:

- perform source identity resolution;
- infer or fuzzy-match product/location identities;
- create or mutate Canonical Truth;
- allocate supply to demand;
- decide whether stock is sufficient for a business policy;
- query or mutate a graph store;
- manufacture evidence or provenance.

Evidence and provenance IDs are caller-supplied lineage references. Their
presence does not make the runtime an evidence adjudicator.

## Why this slice

The existing post-M8 runtime already provides canonical graph, temporal query,
evidence-aware traversal, projection, freshness, and governed query boundaries.
S326 demonstrates that these semantic contracts can support an actual SCM
question without introducing a vendor-specific inventory model.

The intended progression is:

`source data -> governed canonicalization -> canonical inventory facts -> S326 inventory position -> evidence/lineage -> explainable SCM application`

## Follow-up

Future slices can extend this same boundary to demand/supply gap, supplier
delay impact, multi-hop risk, and disruption propagation. Optimization,
allocation, and execution remain separate decision boundaries.
