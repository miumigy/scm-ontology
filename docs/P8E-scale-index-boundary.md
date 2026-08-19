# P8-E — Scale / Index Boundary

## Purpose

P8-E is the **Phase 8 (SCM OS Persistent Graph)** slice that makes the
query / index expectations of the persistent graph explicit and
**backend-neutral**. It answers: *what may a backend index to scale, and how do
we prove that indexing does not leak backend-specific concepts into the
ontology?*

It guarantees that the document-level surface (P8-A) and the backend-level
surface (P8-B relational, P8-C Neo4j) produce **identical query answers** for
identical P8-A documents, so that scale/indexing remains an implementation
concern per the Phase 8 design rule (SCM Ontology ≠ Neo4j).

## Contract

`src/scm_ontology/persistent_query_surface.py`:

- **`PersistentQuerySurface`** — the backend-neutral query contract every
  persistent backend must satisfy:
  - `element_by_id(element_id)` — stable identity lookup;
  - `elements_of_kind(kind)` — node / relationship / version;
  - `elements_effective_at(effective_at)` — temporal-validity lookup
    (effective_at or observed_at);
  - `elements_with_provenance(source_ref)` — provenance / evidence lookup;
  - `element_count()` — cardinality.
- **`DocumentQuerySurface(document)`** — backend-independent baseline: the same
  query answers the same way regardless of what stored the document.
- **`BackedQuerySurface(backend, document_digest)`** — consumes the backend's
  own index-backed query methods, exercising the backend's index.
- **`INDEX_EXPECTATIONS`** — records which predicates a conforming backend may
  index.

### Index expectations (the boundary)

| Predicate | Meaning |
|---|---|
| `element_id` | stable element identity (node / relationship / version) |
| `kind` | node \| relationship \| relationship_version |
| `effective_at` | semantic validity time (relationship_version validity) |
| `source_ref` | provenance / evidence source reference |

A conforming backend may index these. Anything else is backend-specific and not
part of the ontology.

## Behavior

- The relational (P8-B) backend implements the index-backed `element_by_id`,
  `elements_effective_at`, `elements_with_provenance` (in addition to the
  existing `elements_of_kind` / `element_count`).
- The Neo4j (P8-C) backend implements the same query surface.
- Cross-backend equivalence is proven: relational and Neo4j reconstruct the
  same document, so the document-level query surface yields identical answers.

## Fail-closed behavior

P8-E does not add new failure modes: queries against the persistence view are
deterministic. The equivalence guarantee means a backend's index-backed path and
the document baseline can never diverge for a faithfully round-tripped document.

## Truth boundary

A query answers from the **persistence view**, never Canonical Truth. Query
success does not authorize, validate, or promote source evidence into Canonical
Facts (per S311/S312 and the P8-A truth boundary).

## Non-goals

P8-E does not:

- define a specific physical index implementation (SQL or Neo4j specific);
- tune or benchmark query performance;
- perform identity resolution, fuzzy matching, mapping, or Canonical Fact
  application;
- add a database driver or external service (stdlib only);
- mutate Canonical Truth or an external store beyond the injected backend.
