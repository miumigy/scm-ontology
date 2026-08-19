# P8-F — Phase 8 Acceptance

## Purpose

P8-F closes **Phase 8 (SCM OS Persistent Graph)** with a deterministic
acceptance contract: persistent semantics are explicit (P8-A), implemented
interchangeably by relational (P8-B) and Neo4j (P8-C) reference backends,
versioned and replayable (P8-D), and bounded by an explicit scale / index
boundary (P8-E).

P8-F composes the P8-A..P8-E reference paths and probes every capability
deterministically. It performs no external side effect and never mutates
Canonical Truth.

## Contract

`src/scm_ontology/phase8_acceptance.py`:

- **`run_phase8_acceptance(*, accepted_at)`** — runs the Phase 8 capability
  probes and returns an immutable, content-addressed `Phase8AcceptanceReport`
  with an overall `accepted` flag.
- **`Phase8AcceptanceReport`** — the serialized record (`contract_version:
  P8F.1`, `is_phase8_acceptance: true`, per-capability `operable` +
  `evidence_id`, and a deterministic `report_id`).

### Capability inventory (P8-A..P8-E + the P8-F gate)

| key | slice |
|---|---|
| `persistent_graph_contract` | P8-A — explicit persistence semantics |
| `relational_backend` | P8-B — durable SQL-backed backend |
| `neo4j_backend` | P8-C — durable graph-backed backend |
| `snapshot_version_replay` | P8-D — deterministic snapshots + replay |
| `scale_index_boundary` | P8-E — backend-neutral query/index boundary |
| `interchangeable_backends` | P8-F — equivalence gate across backends |

### Phase 8 acceptance criterion

The phase is **accepted** when every capability is operable AND the
`interchangeable_backends` gate holds:

- the relational (P8-B) and Neo4j (P8-C) backends produce **byte-identical**
  P8-A documents for the reference workload;
- **snapshot / version / replay** (P8-D) reproduces the exact document;
- the **query surface** (P8-E) yields identical answers across the backends.

## Fail-closed behavior

- `accepted_at` must be non-empty.
- Any capability probe that raises or returns no usable output is recorded as
  `operable: false` and blocks acceptance (never silently treated as passed).

## Determinism & provenance

- The same `accepted_at` produces an identical report (`report_id` and JSON).
- Each capability retains an `evidence_id` (content hash of its deterministic
  output) for audit / replay.
- The interchangeable-backends gate is deterministic and driver-free (the Neo4j
  backend runs against the in-memory reference transport).

## Non-goals

P8-F does not:

- mutate Canonical Truth, the Canonical Ontology, or the Canonical Graph;
- perform the separate governed application boundary to Canonical Truth;
- add vendor connectors, a Neo4j driver, schedulers, or third-party
  dependencies (stdlib only);
- benchmark or tune physical index performance.
