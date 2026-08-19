# P8-B — Relational Reference Backend

## Purpose

P8-B is the **Phase 8 (SCM OS Persistent Graph)** slice that implements the
P8-A `PersistedGraphDocument` contract on a durable, normalized relational
store. It is the *relational* reference backend in the Phase 8 fan-out:

```text
              Canonical Graph API
                      |
          +-----------+-----------+
          |           |           |
       InMemory     SQL DB      Neo4j
```

P8-B is stdlib-only and backend-neutral: it operates against an injected
`sqlite3` connection (or `:memory:` for deterministic tests), so no external
database driver or service is required and the semantic core stays portable to
other relational engines with an equivalent cursor contract.

## Contract

`src/scm_ontology/relational_graph_backend.py` — `RelationalGraphBackend(conn)`:

- **`write(document)`** — persists a P8-A `PersistedGraphDocument` atomically in
  one transaction, content-addressed by `document_digest`, idempotent on
  re-write.
- **`read(document_digest)`** — reconstructs a `PersistedGraphDocument` from
  relational rows, preserving payload, temporal fields, element order, and
  provenance.
- **`contains` / `list_document_digests`** — presence / listing queries.
- **`element_count` / `elements_of_kind(document_digest, kind)`** — indexed
  element queries (the foundation P8-E builds on).

### Relational schema (normalized, element-indexed)

| Table | Purpose |
|---|---|
| `documents` | content-addressed document root (`document_digest` PK, `scope`, `canonical_digest`) |
| `elements` | one row per P8-A element (`node` / `relationship` / `relationship_version`) with payload, temporal fields, and a `position` column preserving document order |
| `element_provenance` | explicit `EvidenceRef` provenance rows keyed by element |

`element_id` and `kind` are first-class indexed columns, so a relational store
can scale and index without leaking backend concepts into the ontology (P8-E).

## Guarantees

- **durable** — `write` commits atomically across all rows;
- **content-addressed** — `document_digest` is the immutable primary key and is
  re-validated on write (fail closed on mismatch);
- **idempotent** — re-writing the same digest does not duplicate data;
- **round-trip faithful** — `write -> read` produces a byte-identical
  `PersistedGraphDocument` (payload, temporal fields, provenance, and element
  order), so interchangeable backends produce equivalent semantics (P8-F).

## Fail-closed behavior

P8-B MUST reject:

- a non-`PersistedGraphDocument` input;
- an empty `document_digest`;
- a supplied digest that does not match the document (tampering / mismatch);
- any relational integrity failure (rolled back, never partially persisted).

## Truth boundary

Persistence success means **relational storage succeeded**. It does not
authorize, validate, or promote source evidence into Canonical Facts (per
S311/S312 and the P8-A truth boundary).

## Non-goals

P8-B does not:

- perform identity resolution, fuzzy matching, mapping, or Canonical Fact
  application;
- add a vendor database driver or external service (stdlib `sqlite3` only);
- define backend-specific indexes beyond the element/kind indexing needed for
  equivalent query semantics;
- mutate Canonical Truth or any external store beyond the supplied connection.
