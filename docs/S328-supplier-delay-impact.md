# S328 — Canonical Supplier Delay Impact

## Purpose

S328 is a Phase 4 business-question vertical slice that derives supplier schedule delay from already-canonical supplier commitments and delay events.

## Contract

For an exact `(supplier_id, item_id, unit)` scope:

`delay_days = max(actual_at - expected_at, 0)`

where timestamps begin with ISO calendar dates. A delay event without an exact canonical commitment scope is not attached to another commitment.

## Semantic boundary

S328 MUST NOT:

- perform supplier or item identity resolution;
- fuzzy-match or infer commitments;
- mutate Canonical Truth;
- allocate demand or supply;
- choose alternative suppliers or expedites;
- query or mutate a graph store;
- manufacture evidence or provenance.

Evidence and provenance IDs are caller-supplied lineage references.

## Result

The runtime emits `contract_version: S328.1` and deterministic UTF-8 JSON. The result is a derived observation, not a decision or authorization.

## Why this slice

S326 established inventory position and S327 established demand/supply gap. S328 extends the same read-only business-question boundary to supplier delay, creating a foundation for later supplier impact, multi-hop risk, and disruption propagation without collapsing analysis into operational decisions.
