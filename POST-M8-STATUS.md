# Post-M8 implementation status

## Current phase

**Phase 8 — SCM OS Persistent Graph: COMPLETE (P8-A..P8-F).**

P8-A (`src/scm_ontology/persistent_graph_contract.py`) defines the explicit,
backend-neutral persistence semantics — nodes, relationships, temporal state,
evidence, and provenance — as a content-addressed `PersistedGraphDocument`
anchored to the source `CanonicalGraph`. It is the contract that the P8-B/P8-C
backends and P8-F acceptance conform to, and it never mutates Canonical Truth.
See `docs/P8A-persistent-graph-contract.md`. **P8-B (Relational Reference
Backend, `src/scm_ontology/relational_graph_backend.py`)** implements that
contract on a durable, normalized relational store (`sqlite3`-based, stdlib
only): `write` persists a `PersistedGraphDocument` atomically and
content-addressed, `read` reconstructs it byte-identically (preserving payload,
temporal fields, element order, and provenance), and element/kind indexing
provides the foundation P8-E builds on. See `docs/P8B-relational-backend.md`.
**P8-C (Neo4j Reference Backend, `src/scm_ontology/neo4j_graph_backend.py`)** implements the same
interchangeable `PersistentGraphBackend` interface as graph-shaped storage
(driver-free, injected Cypher executor/query), preserving the same P8-A semantics
and producing equivalent canonical/query results to P8-B — proving the P8-F
interchangeability premise. See `docs/P8C-neo4j-backend.md`. **P8-D (Snapshot /
Version / Replay, `src/scm_ontology/persistent_snapshot.py`)** wraps any
`PersistentGraphBackend` with an immutable, content-addressed version index and
deterministic replay of any recorded version (including reconstructing the
underlying `CanonicalGraph`). See `docs/P8D-snapshot-version-replay.md`.

For completeness, Phase 7 (previous) is recorded below.

---

## Phase 7 — SCM OS Real Data Plane (COMPLETE)

The SCM OS reference platform moves from in-memory fixtures toward
heterogeneous enterprise data while preserving the Canonical Truth boundary.
The first slice implements a **Reference Data Adapter** (P7-A): portable
CSV/JSON/SQL source adapters
(`src/scm_ontology/reference_data_adapter.py`) that turn arbitrary enterprise
representations into immutable, provenance-bearing `SourceEvidence` records.
All adapters are fail-closed, carry field-level `EvidenceRef` provenance, carry
an explicit `SourceManifest` (source system, adapter/mapping versions, scope,
extraction time), and never map, resolve identity, or mutate Canonical Truth.
See `docs/P7A-reference-data-adapter.md`. The **P7-B Mapping/Canonicalization
Runtime** (`src/scm_ontology/mapping_canonicalization_runtime.py`) consumes that
evidence and emits S262-compatible, deterministic `CanonicalizationResult`
records (entity/attribute/predicate mapping per S256/S257/S258, S255 semantic-gap
classification, `canonical_mutation = False`). See `docs/P7B-mapping-canonicalization.md`. The **P7-C Identity Resolution Runtime** (`src/scm_ontology/identity_resolution_runtime.py`) decides whether distinct source identities refer to the same Canonical Entity with deterministic, governed conflict handling (S279/S280/S288/S290/S297), preserving source identity, provenance, evidence, and append-only decisions. See `docs/P7C-identity-resolution-runtime.md`. The **P7-D Data Quality / Freshness Gate** (`src/scm_ontology/data_quality_gate.py`) validates completeness, freshness, scope, unit, and provenance of `SourceEvidence` before canonicalization (fail closed, read-only). See `docs/P7D-data-quality-gate.md`. The **P7-E Multi-source Reference Dataset** (`src/scm_ontology/multi_source_reference.py`) composes P7-A→P7-D so several heterogeneous sources converge onto one reproducible, traceable reference Canonical Graph (never Canonical Truth). See `docs/P7E-multi-source-reference-dataset.md`. **P7-F (Phase 7 acceptance, `src/scm_ontology/phase7_acceptance.py`)** probes all five slices and confirms heterogeneous input -> governed canonicalization produces a reproducible, traceable reference Canonical Graph (`accepted = True`), closing Phase 7. See `docs/P7F-phase7-acceptance.md`.

Phase 6 (previous):

The SCM OS reference capabilities are now discoverable and operable from one
coherent control-plane surface. Merged slices (PR #395–#400):

- P6-A — SCM OS Cockpit v0 (`src/scm_ontology/scm_os_cockpit.py`);
- P6-B — Decision Inbox (`src/scm_ontology/decision_inbox.py`);
- P6-C — Simulation/Optimization Workspace (`src/scm_ontology/sim_optim_workspace.py`);
- P6-D — Execution Workflow Workspace (`src/scm_ontology/execution_workspace.py`);
- P6-E — Control Plane E2E (`src/scm_ontology/control_plane_e2e.py`);
- P6-F — Phase 6 acceptance (`src/scm_ontology/phase6_acceptance.py`, `run_phase6_acceptance`).

Preceding capability phases are also complete: Phase R1–R5 runtime + Phase 5
SCM OS integration through S366.

## Next phase

**Phase 8 — SCM OS Persistent Graph: COMPLETE** (P8-A..P8-F merged). The next
phase per `docs/roadmap-post-m8.md` is **Phase 9 — Closed-Loop SCM OS
Execution**.

## Guardrails (still in force)

Do not collapse canonicalization / identity-resolution into each other, and do
not weaken the M8 boundaries. A canonical concept match is not proof that two
source records refer to the same enterprise object. Implement against the M8
contracts; treat normative M8 documents as contracts for future implementations.
