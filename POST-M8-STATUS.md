# Post-M8 implementation status

## Current phase

**Phase 7 — SCM OS Real Data Plane: IN PROGRESS (P7-A complete).**

The SCM OS reference platform moves from in-memory fixtures toward
heterogeneous enterprise data while preserving the Canonical Truth boundary.
The first slice implements a **Reference Data Adapter** (P7-A): portable
CSV/JSON/SQL source adapters
(`src/scm_ontology/reference_data_adapter.py`) that turn arbitrary enterprise
representations into immutable, provenance-bearing `SourceEvidence` records.
All adapters are fail-closed, carry field-level `EvidenceRef` provenance, carry
an explicit `SourceManifest` (source system, adapter/mapping versions, scope,
extraction time), and never map, resolve identity, or mutate Canonical Truth.
See `docs/P7A-reference-data-adapter.md`.

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

## Next slice

**Phase 7 — SCM OS Real Data Plane.** Move from reference/in-memory fixtures
toward heterogeneous enterprise data while preserving the Canonical Truth
boundary. Per `docs/roadmap-post-m8.md`, the next slice is **P7-A — Reference
Data Adapter** (CSV/JSON/SQL adapters with explicit source evidence), followed
by P7-B (Mapping/Canonicalization Runtime), P7-C (Identity Resolution Runtime),
P7-D (Data Quality/Freshness Gate), P7-E (Multi-source Reference Dataset), and
P7-F (Phase 7 acceptance).

## Guardrails (still in force)

Do not collapse canonicalization / identity-resolution into each other, and do
not weaken the M8 boundaries. A canonical concept match is not proof that two
source records refer to the same enterprise object. Implement against the M8
contracts; treat normative M8 documents as contracts for future implementations.
