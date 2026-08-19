# Post-M8 implementation status

## Current phase

**Phase 10 — Autonomous SCM Control: COMPLETE (P10-A..P10-G).**

Phase 9 (Closed-Loop Execution, P9-A..P9-G COMPLETE — full record below) hands
off to **Phase 10 — Autonomous SCM Control** (see `docs/roadmap-post-m8.md`).
The goal is to introduce agentic/autonomous reasoning only after Truth,
Governance, Execution, and Outcome semantics are stable, keeping the agent
inside the governed loop:

```text
Observe -> Reason -> Propose -> Simulate -> Evaluate -> Authorize
  -> Execute -> Observe Outcome -> Learn
```

Phase 10 establishes the agent boundaries that surround the now-stable
governed loop: scoped evidence-aware observations (P10-A), proposal-only agent
tools (P10-B), simulation-before-execution (P10-C), policy-aware autonomy
(P10-D), explicit human-in-the-loop control (P10-E), and agent replay/audit
(P10-F). P10-G composes these into an acceptance report that closes the phase
with `accepted = True`.

**P9-A (Execution Outcome Contract,
`src/scm_ontology/execution_outcome_contract.py`)** establishes the explicit
success/failure/partial outcome model with evidence and provenance: a command
may produce one or more per-target `ResultElement` records (each carrying its
own status, evidence, and external reference) aggregated into a phase verdict
(`success` / `partial` / `failure` / `rejected`), content-addressed and
replay-reproducible. See `docs/P9A-execution-outcome-contract.md`. **P9-B
(External Execution Adapter, `src/scm_ontology/external_execution_adapter.py`)**
introduces the bounded boundary through which a governed `ExecutionCommand` may
cause side effects in an external system: an `ExternalExecutionAdapter` protocol
with a deterministic `ReferenceExternalExecutionAdapter` test double and an
`InMemoryExternalSystem` fake target system (see
`docs/P9B-external-execution-adapter.md`). **P9-C (Approval-to-Execution
Runtime, `src/scm_ontology/approval_to_execution_runtime.py`)** advances an
approved command from a dry-run to controlled execution through the P9-B
adapter gate, records every S355 lifecycle transition (dry_run -> executing ->
executed), and captures the immutable P9-A outcome (see
`docs/P9C-approval-to-execution-runtime.md`). **P9-D (Outcome-to-Event
Canonicalization, `src/scm_ontology/outcome_to_event_canonicalization.py`)** projects a
governed outcome into a read-only `CanonicalEvent` (execution_outcome_recorded)
only when the command lifecycle reached the executed state, embedding the
governance chain and outcome evidence/provenance (see
`docs/P9D-outcome-to-event-canonicalization.md`). **P9-E (Closed-Loop E2E,
`src/scm_ontology/closed_loop_e2e.py`)** composes the governed loop end to end —
state → decision → authorization → execution → outcome → canonical event →
updated state — where the operative `ClosedLoopState` is an explicit derived
snapshot that is updated only through the governed execution/event boundary (see
`docs/P9E-closed-loop-e2e.md`). **P9-F (Failure / Retry / Idempotency,
`src/scm_ontology/failure_retry_idempotency.py`)** adds idempotency /
duplicate-command protection (a command id executes at most once), bounded retry
of transient failures, partial-execution handling (a partial outcome is never
redone), and recovery semantics that escalate to `failed_permanently` with a
`RecoverySignal` when retries are exhausted (see
`docs/P9F-failure-retry-idempotency.md`). **P9-G (Phase 9 acceptance,
`src/scm_ontology/phase9_acceptance.py`)** composes a reference governed closed
loop against the injected external system and confirms every P9-A..P9-F
capability is operable (`accepted = True`; see
`docs/P9G-phase9-acceptance.md`). **Phase 9 is COMPLETE.**

---

## Phase 10 — Autonomous SCM Control (COMPLETE)

Phase 10 introduces **bounded autonomy inside the governed loop**. AI is a
Reasoning Provider / Agent, not the SCM OS: agents observe scoped projections
and propose actions, while governance authorizes and execution adapters perform
side effects. Every agent step is replayable and non-mutating.

- **P10-A (Agent Observation Boundary, `src/scm_ontology/agent_observation.py`)** —
  agents receive scoped, evidence-aware, read-only `AgentObservation`s composed
  from an already-validated `GraphProjection` through the S338/S339 read path.
  The envelope is immutable, content-addressed, bound to an `AgentScope`
  (`agent_id`, `question_id`, `node_type`, `node_id`, `relationship_type`), and
  exposes `can_write = False` — no mutation surface. See
  `docs/P10A-agent-observation-boundary.md`.
- **P10-B (Tool / Action Boundary, `src/scm_ontology/agent_tool.py`)** — agent
  tools produce content-addressed `AgentProposal` records (never canonical
  mutations) via `run_agent_tool`, and `proposal_to_execution_command` routes a
  proposal through S344 validation and S345 authorization before any
  `ExecutionCommand` may be produced. See `docs/P10B-tool-action-boundary.md`.
- **P10-C (Simulation-before-Execution,
  `src/scm_ontology/simulation_before_execution.py`)** — material decisions are
  evaluated against the S363 deterministic governed simulation before
  authorization; `evaluate_simulation_before_execution` produces a
  content-addressed `AgentSimulationEvaluation` (`feasible` verdict) that
  informs, but never overrides, governance. See
  `docs/P10C-simulation-before-execution.md`.
- **P10-D (Policy-aware Autonomy, `src/scm_ontology/policy_autonomy.py`)** —
  confidence, risk, monetary impact, and scope determine the allowed autonomy
  level via `evaluate_autonomy`/`AutonomyPolicy`, yielding
  `fully_autonomous`/`approved`/`human_review`/`blocked`. Fails closed on
  unknown scope or threshold violations. See `docs/P10D-policy-aware-autonomy.md`.
- **P10-E (Human-in-the-loop Control, `src/scm_ontology/human_control.py`)** —
  explicit review, override, escalation, and delegation paths via
  `route_human_control`, recording each outcome as a replayable
  `HumanControlRecord` (approval or senior override). See
  `docs/P10E-human-in-the-loop-control.md`.
- **P10-F (Agent Replay / Audit, `src/scm_ontology/agent_replay.py`)** — every
  agent observation, proposal, autonomy verdict, human-control record, command,
  and outcome is recorded in a content-addressed, append-only `AgentAuditTrail`;
  `replay()` verifies content integrity and detects tampering. See
  `docs/P10F-agent-replay-audit.md`.
- **P10-G (Phase 10 acceptance, `src/scm_ontology/phase10_acceptance.py`)** —
  `run_phase10_acceptance` probes all six capabilities and the governed
  autonomous-loop gate, returning `accepted = True`. The gate runs a bounded,
  fully-autonomous replenishment use case through observe -> propose -> evaluate
  -> human-control -> replayable audit while remaining governed. See
  `docs/P10G-phase10-acceptance.md`.

**Phase 10 is COMPLETE.** Autonomy is a policy result, human governance remains
explicit, and the agent never owns Canonical Truth.

---

## Phase 8 — SCM OS Persistent Graph (COMPLETE)

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

**Phase 9 — Closed-Loop SCM OS Execution: COMPLETE** (P9-A..P9-G merged). The
next phase per `docs/roadmap-post-m8.md` is **Phase 10 — Autonomous SCM
Control**: bounded, governed AI autonomy that observes scoped evidence, proposes
via tool/action boundaries, simulates before executing, and remains replayable
and governed. To continue in a new session, start from
`docs/SCM_OS_HANDOFF_PROMPT_PHASE10.md` (Phase 10 new-session handoff prompt).

## Guardrails (still in force)

Do not collapse canonicalization / identity-resolution into each other, and do
not weaken the M8 boundaries. A canonical concept match is not proof that two
source records refer to the same enterprise object. Implement against the M8
contracts; treat normative M8 documents as contracts for future implementations.
