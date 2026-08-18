# P8-A — Persistent Graph Contract

## Purpose

P8-A is the first **Phase 8 (SCM OS Persistent Graph)** slice. It defines the
**explicit persistence semantics** that every backend must preserve — nodes,
relationships, temporal state, evidence, and provenance — while remaining
transport-neutral. Phase 8 turns the Canonical Graph runtime into a
persistence-independent production reference architecture:

```text
              Canonical Graph API
                      |
          +-----------+-----------+
          |           |           |
       InMemory     SQL DB      Neo4j
```

P8-A is the contract layer underneath that fan-out. It does **not** introduce a
database dependency or vendor schema. Later slices implement the same contract:
P8-B relational backend, P8-C Neo4j backend, P8-D snapshot/replay, P8-E
index/scale boundary.

## Contract

`src/scm_ontology/persistent_graph_contract.py`:

- **`PersistedElement`** — one element of the persistence view with an explicit
  `kind` (`node` | `relationship` | `relationship_version`), a stable
  `element_id`, a structural `payload`, separated temporal fields
  (`effective_at`, `valid_to`, `observed_at`), and explicit `provenance`
  (`EvidenceRef`) attachments.
- **`PersistedGraphDocument`** — the content-addressed, backend-neutral
  persistence view of a `CanonicalGraph` anchored to the source graph via
  `canonical_digest`.
- **`persistent_graph_document(graph, *, scope, provenance)`** — builds the
  document deterministically.
- **`persistence_element_id(kind, identity)`** — the stable identity under
  which a backend stores an element.
- **`document_from_mapping(value)`** — restores a document, recomputing and
  validating the content digest (fail closed).

### Explicit persistence semantics

| Semantic | How it is preserved |
|---|---|
| Node | `kind=node`, payload carries `node_id`, `node_type`, `properties` |
| Relationship | `kind=relationship`, payload carries endpoints and predicate |
| Temporal state | each relationship version is a distinct `relationship_version` element carrying `effective_at` / `valid_to` / `observed_at` — never collapsed into a current edge |
| Evidence / provenance | explicit `EvidenceRef` attachments on any element; never implied Canonical Truth |
| Scope | required, non-empty governed persistence scope (per S311) |

## Determinism & provenance

- Identical `(graph, scope, provenance)` produces an identical
  `PersistedGraphDocument` (`document_digest` and JSON), content-addressed for
  audit and replay.
- `canonical_digest` anchors the document to the source `CanonicalGraph` so a
  backend verifies it persists the intended graph.

## Fail-closed behavior

P8-A MUST reject:

- an empty `scope`;
- an unsupported `kind` or empty `element_id`;
- a relationship endpoint whose node is not present in the graph (dangling
  reference);
- a `document_from_mapping` whose supplied digest does not match the recomputed
  content digest.

## Truth boundary

The persisted document is the **persistence view**, never Canonical Truth.
Storage success does not authorize, validate, or promote source evidence into
Canonical Facts (per S311/S312 guardrails).

## Non-goals

P8-A does not:

- perform identity resolution, fuzzy matching, mapping, or Canonical Fact
  application;
- add a database driver, vendor connector, or web dependency (stdlib only);
- define backend-specific indexes or storage layouts (that is P8-E and the
  individual backends);
- mutate Canonical Truth or any external store (read-only contract).
