# SCM OS — New Session Handoff Prompt (Phase 9)

Continue the user's `miumigy/scm-ontology` project as the implementation AI.

## Where the project is

**Phase 8 — SCM OS Persistent Graph: COMPLETE (P8-A..P8-F merged).**

The Canonical Graph runtime is now a persistence-independent reference
architecture. The next phase is **Phase 9 — Closed-Loop SCM OS Execution**
(see `docs/roadmap-post-m8.md`):

```text
Observation -> Canonical Graph -> Reasoning -> Decision -> Authorization
  -> ExecutionCommand -> External Execution -> Execution Outcome
  -> Canonical Event -> Canonical Graph -> Next Decision
```

## What Phase 8 delivered (all merged)

- **P8-A** `persistent_graph_contract.py` — explicit, backend-neutral persistence semantics (nodes, relationships, temporal state, evidence, provenance) as a content-addressed `PersistedGraphDocument`.
- **P8-B** `relational_graph_backend.py` — durable `sqlite3` relational backend (`PersistentGraphBackend` interface).
- **P8-C** `neo4j_graph_backend.py` — driver-free Neo4j backend + `InMemoryNeo4jTransport` reference transport.
- **P8-D** `persistent_snapshot.py` — immutable `VersionedGraphBackend` (capture / replay / list_versions).
- **P8-E** `persistent_query_surface.py` — backend-neutral query/index boundary + `INDEX_EXPECTATIONS`; relational and Neo4j give identical answers.
- **P8-F** `phase8_acceptance.py` — `run_phase8_acceptance` returns `accepted=True` (6/6 operable, interchangeable-backends gate).

## Core principles (unchanged)

1. **AI may propose; governance authorizes; execution adapters perform side effects.**
2. No application may mutate Canonical Truth directly; all mutations must enter through the execution/event boundary and remain auditable.
3. Never weaken Canonical Truth, provenance, temporal, lifecycle, or governance boundaries (per `AGENTS.md`).
4. Fail closed; preserve immutable/deterministic contracts; stdlib-only unless a driver is injected.

## Phase 9 milestones (from roadmap)

- [ ] **P9-A — Execution Outcome Contract**: explicit success/failure/partial outcome model with evidence and provenance;
- [ ] **P9-B — External Execution Adapter**: injected side-effect adapter boundary with deterministic test double;
- [ ] **P9-C — Approval-to-Execution Runtime**: authorized commands can progress from dry-run to controlled execution;
- [ ] **P9-D — Outcome-to-Event Canonicalization**: execution outcomes become canonical events without bypassing governance;
- [ ] **P9-E — Closed-Loop E2E**: state -> decision -> authorization -> execution -> outcome -> canonical event -> updated state;
- [ ] **P9-F — Failure / Retry / Idempotency**: bounded retry, duplicate-command protection, partial execution handling, recovery semantics;
- [ ] **P9-G — Phase 9 acceptance**: a reference SCM workflow can operate as a governed closed loop against an injected external system.

## Existing contracts Phase 9 builds on

`execution_command.py`, `execution_runtime.py` (side-effect-free dry run),
`execution_boundary.py`, `execution_outcome.py`, `execution_outcome_event.py`,
`execution_event.py`, `execution_trace.py`, `command_lifecycle.py`,
`governed_audit.py` (S354), `canonical_event.py`, `event.py`,
`closed_loop_runtime.py`, `closed_loop_snapshot.py`, plus the post-M8 governed
loop (`graph_query.py`, `graph_projection.py`, `reasoning_assembly.py`,
`reasoning_provider.py`, `reasoning_output.py`, `proposal_validation.py`,
`decision_authorization.py`, `execution_command.py`).

The S366 `operational_workflow.py` already composes governed audit + command
lifecycle to the dry-run state; Phase 9 extends that toward real external
execution and back to canonical events.

## Recommended first slice

**P9-A — Execution Outcome Contract** is the natural smallest next milestone:
an explicit success/failure/partial outcome model with evidence and provenance,
extending the existing dry-run `execution_runtime` toward real outcomes.

## Suggested workflow for a new session

1. `git checkout main && git pull` — inspect latest `main` and CI (Phase 8 is merged; verify `python -m scm_ontology.validator`).
2. `git status` / `gh pr list` — confirm no stale branches or open PRs (none currently).
3. Re-read `AGENTS.md`, `docs/roadmap-post-m8.md`, and this handoff.
4. Implement the chosen milestone following the repo loop:
   inspect -> model -> contract -> implement -> validate -> test -> document -> PR -> governed merge
5. One PR per slice; update `POST-M8-STATUS.md`, the roadmap checklist, `docs/README.md`, and README with each slice.
6. Keep historical milestone docs intact; only correct them for genuine fact corrections.
