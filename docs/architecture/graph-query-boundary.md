# S338 — Canonical Graph Query Boundary

S338 defines a storage-neutral query boundary over the immutable S337 `GraphProjection`.

## Contract

`query_nodes()` performs exact matching by canonical `node_id` and/or `node_type`.
`query_relationships()` performs exact matching by relationship type and/or endpoint node identity.

Results retain the projection provenance IDs and serialize deterministically as `S338.1` JSON with UTF-8 characters preserved.

## Explicit non-goals

S338 does not mutate a graph store, perform identity resolution, infer relationships, traverse an external database, or execute business decisions.

The intended architecture is:

Canonical Model → Graph Projection (S337) → Graph Query (S338) → Business Question / Decision Context.
