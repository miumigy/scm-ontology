# P8-D — Snapshot / Version / Replay

## Purpose

P8-D is the **Phase 8 (SCM OS Persistent Graph)** slice that adds deterministic,
replayable versioning on top of any persistent graph backend. It answers:
*which version of a graph was in effect when, and can I reproduce it exactly?*

It builds on P8-A (`PersistedGraphDocument`), P8-B / P8-C (interchangeable
backend), and the existing `canonical_graph_persistence` versioning concept —
but scoped to the persistent graph view and made backend-neutral.

## Contract

`src/scm_ontology/persistent_snapshot.py`:

- **`PersistentSnapshot`** — immutable, content-addressed capture of one graph
  version (`snapshot_id`, `graph_id`, `version`, `document_digest`, metadata).
- **`VersionedGraphBackend(backend)`** — wraps any `PersistentGraphBackend`
  (relational P8-B, Neo4j P8-C) and records an append-only version index.
  - **`capture(document, *, graph_id, version, created_at)`** — persists the
    document through the backend and records a deterministic snapshot.
  - **`replay(graph_id, version)`** — reproduces the exact
    `PersistedGraphDocument` for a recorded version.
  - **`replay_graph(graph_id, version)`** — reconstructs the underlying
    `CanonicalGraph`.
  - **`list_versions` / `latest_version` / `snapshot`** — version queries.

## Guarantees

- **deterministic** — identical `(document, graph_id, version, created_at)`
  yields an identical `snapshot_id` and replay output across runs and backends;
- **replayable** — any recorded version reproduces the exact document;
- **immutable / append-only** — recorded versions cannot be mutated or rewritten
  with a different document;
- **backend-neutral** — works against the relational (P8-B), Neo4j (P8-C), or
  any `PersistentGraphBackend`.

## Fail-closed behavior

P8-D MUST reject:

- an empty `graph_id` or `version`;
- a non-`PersistedGraphDocument` / empty-digest document;
- a version collision — re-capturing an already-recorded version with a
  *different* document;
- a replay request for a missing version or an unknown graph.

## Truth boundary

A snapshot is a **persistence-view capture**, never Canonical Truth. Replay does
not authorize, validate, or promote source evidence into Canonical Facts (per
S311/S312 and the P8-A truth boundary).

## Non-goals

P8-D does not:

- perform identity resolution, fuzzy matching, mapping, or Canonical Fact
  application;
- add a database driver or external service (stdlib only);
- define backend-specific index or scaling rules (that is P8-E);
- mutate Canonical Truth or an external store beyond the wrapped backend.
