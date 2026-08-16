# S331 — Canonical Network Disruption Propagation

## Purpose

S331 is a Phase 4 business-question vertical slice that propagates an explicit disruption observation across explicitly declared directed supply dependencies.

## Contract

For each declared dependency:

`next_impact = current_impact * propagation_factor`

The initial impact is the canonical disruption `severity`, constrained to `[0, 1]`. Traversal is bounded by an explicit `max_hops`.

## Semantic boundary

S331 MUST NOT:

- infer network relationships;
- perform identity resolution;
- traverse reverse relationships;
- mutate Canonical Truth or graph storage;
- allocate demand or supply;
- optimize operations;
- recommend mitigation;
- manufacture evidence or provenance.

Dependencies and disruption observations are caller-supplied canonical facts. Cycles are not traversed.

## Scope

Dependencies are directed from `upstream_node_id` to `downstream_node_id`. The runtime preserves the explicit path and hop count for every derived impact.

## Result

The runtime emits `contract_version: S331.1` and deterministic UTF-8 JSON. Evidence and provenance identifiers from the originating disruption observation are preserved in the derived result.
