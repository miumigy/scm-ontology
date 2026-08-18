# P8-C — Neo4j Reference Backend

## Purpose

P8-C is the **Phase 8 (SCM OS Persistent Graph)** slice that implements the P8-A
`PersistedGraphDocument` contract as a durable, graph-backed reference backend.
It is the *graph-backed* sibling of the P8-B relational backend (and the
in-memory reference store), so P8-F can prove that interchangeable persistence
backends produce equivalent canonical/query semantics for the same P8-A document.

```text
              Canonical Graph API
                      |
          +-----------+-----------+
          |           |           |
       InMemory     SQL DB      Neo4j   (P8-C)
```

## Boundary (driver-free)

The semantic core does **not** import the Neo4j driver. The application injects
two transport callables — `execute(statement, params)` for writes and
`query(statement, params) -> rows` for reads — so driver / session / transaction
lifecycle stays outside the ontology. A deterministic in-memory test double
provides the transport for tests.

## Contract

`src/scm_ontology/neo4j_graph_backend.py` — `Neo4jGraphBackend(execute, query)`
implements the same interchangeable `PersistentGraphBackend` interface as the
P8-B `RelationalGraphBackend`:

- **`write(document)`** — persists a P8-A document, content-addressed and
  idempotent, emitting MERGE statements for documents, elements, and
  provenance.
- **`read(document_digest)`** — reconstructs a byte-identical
  `PersistedGraphDocument` from nodes and HAS_PROVENANCE relationships.
- **`contains` / `list_document_digests` / `element_count` /
  `elements_of_kind`** — the same query surface as P8-B.

### Neo4j data model (graph-shaped)

- `(:CanonicalDocument {document_digest, scope, canonical_digest})`
- `(:CanonicalElement {document_digest, position, element_id, kind, payload,
  effective_at, valid_to, observed_at})`
- `(:CanonicalElement)-[:HAS_PROVENANCE {observed_at, metadata}]->
  (:CanonicalProvenance {source_ref})`

Provenance is modeled as relationships, while P8-B models it as rows — the two
backends are storage-shape-different but semantic-equivalent.

## Guarantees

- deterministic, content-addressed write (`document_digest` re-validated);
- idempotent re-write (no duplicate data);
- byte-identical `write -> read` round-trip preserving payload, temporal fields,
  element order, and provenance;
- **equivalence with P8-B**: identical canonical/query semantics for the same
  P8-A document.

## Fail-closed behavior

P8-C MUST reject:

- a non-`PersistedGraphDocument` input;
- an empty `document_digest`;
- a supplied digest that does not match the document;
- a missing `document_digest` on read, or a duplicate document on read.

## Truth boundary

Persistence success means **graph-store storage succeeded**. It does not
authorize, validate, or promote source evidence into Canonical Facts (per
S311/S312 and the P8-A truth boundary).

## Non-goals

P8-C does not:

- import the Neo4j driver or bind the ontology to a database vendor;
- perform identity resolution, fuzzy matching, mapping, or Canonical Fact
  application;
- define backend-specific indexes beyond element/kind (that is P8-E);
- mutate Canonical Truth or any external store beyond the injected transport.
