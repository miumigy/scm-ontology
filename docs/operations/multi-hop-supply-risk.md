# S329 — Canonical Multi-Hop Supply Risk

## Purpose

S329 is a Phase 4 business-question vertical slice that derives downstream supply risk from already-canonical risk observations and explicitly declared supply dependencies.

## Contract

For each observed upstream node, risk is propagated over directed canonical dependencies for at most `max_hops` hops. The reported score is the maximum explicitly observed upstream risk reachable along a declared path.

`0 <= risk_score <= 1`

The score is a semantic risk observation, not a probability, forecast, or mitigation recommendation.

## Semantic boundary

S329 MUST NOT:

- infer or reverse dependency relationships;
- perform identity resolution;
- mutate Canonical Truth or a graph store;
- allocate supply or demand;
- optimize mitigation;
- choose suppliers, routes, or expedites;
- manufacture evidence or provenance.

Dependencies and lineage identifiers are caller-supplied canonical facts.

Cycles are not traversed. `max_hops` is explicit and must be at least one.

## Result

The runtime emits `contract_version: S329.1` and deterministic UTF-8 JSON. Each result preserves its explicit path, hop count, and consulted evidence/provenance identifiers.

## Why this slice

S326 established inventory position, S327 demand/supply gap, and S328 supplier schedule delay. S329 composes the graph semantics into a first multi-hop risk observation while keeping causal interpretation and mitigation decisions outside the canonical semantic runtime.
