# S337 — Graph Projection Boundary

## Purpose

S337 defines a deterministic projection from canonical semantic objects into a graph-shaped representation. It is a projection contract, not a graph database integration.

## Contract

`GraphProjection` contains:

- `nodes[]`
- `relationships[]`
- `provenance_ids[]`

Each node has a stable `node_id`, `node_type`, and properties. Each relationship has a stable `relationship_id`, `relationship_type`, source and target node IDs, and properties.

## Invariants

- node IDs are unique
- relationship IDs are unique
- relationship endpoints must reference projected nodes
- provenance IDs are deduplicated and deterministically ordered
- node and relationship output is deterministically ordered
- JSON preserves UTF-8 characters

## Explicit non-goals

S337 does not:

- mutate a graph store
- resolve identities
- infer relationships
- infer causality
- perform traversal
- modify canonical truth

The graph representation is therefore a **projection of canonical meaning**, not a second source of truth.

## Contract version

`S337.1`
