# SCM OS — New Session Handoff Prompt (Phase 10)

Continue the user's `miumigy/scm-ontology` project as the implementation AI.

## Where the project is

**Phase 9 — Closed-Loop SCM OS Execution: COMPLETE (P9-A..P9-G merged).**

The governed real-execution loop is now stable and deterministic: a reference
SCM workflow observes -> reasons -> decides -> authorizes -> executes against an
injected external system -> captures the outcome as a canonical event -> updates
derived state, with idempotency / retry / recovery semantics. The next phase is
**Phase 10 — Autonomous SCM Control** (see `docs/roadmap-post-m8.md`):

```text
Observe -> Reason -> Propose -> Simulate -> Evaluate -> Authorize
  -> Execute -> Observe Outcome
```

## What Phase 9 delivered (all merged)

- **P9-A** `execution_outcome_contract.py` — explicit success/partial/failure/rejected outcome model with per-target `ResultElement`, evidence & provenance, content-addressed.
- **P9-B** `external_execution_adapter.py` — injectable `ExternalExecutionAdapter` boundary + deterministic `ReferenceExternalExecutionAdapter` test double and `InMemoryExternalSystem` fake target.
- **P9-C** `approval_to_execution_runtime.py` — authorized commands progress `dry_run -> executing -> executed` with fail-closed gates.
- **P9-D** `outcome_to_event_canonicalization.py` — governed outcomes become `CanonicalEvent`s only via the executed governed path.
- **P9-E** `closed_loop_e2e.py` — full governed loop: state -> decision -> authorization -> execution -> outcome -> canonical event -> updated derived state (`ClosedLoopState`, `derived=True`).
- **P9-F** `failure_retry_idempotency.py` — idempotency / duplicate-command protection, bounded retry, partial-never-redone, recovery escalation (`ExecutionRunRegistry`, `RetryableAdapter`).
- **P9-G** `phase9_acceptance.py` — `run_phase9_acceptance` returns `accepted=True` (7/7 operable, governed closed-loop gate).

## Core principles (unchanged, reinforced for AI)

1. **AI is a Reasoning Provider / Agent, not the SCM OS.** AI proposes; governance authorizes; execution adapters perform side effects. AI must never become the owner of Canonical Truth — the OS owns state, governance, authorization, and execution boundaries.
2. Agents observe scoped, evidence-aware projections — never unrestricted canonical-graph mutation access.
3. Agent tools produce proposals or `ExecutionCommand`s, never direct canonical mutations.
4. No application may mutate Canonical Truth directly; all mutations enter through the execution/event boundary and remain auditable.
5. Never weaken Canonical Truth, provenance, temporal, lifecycle, or governance boundaries (per `AGENTS.md`).
6. Fail closed; preserve immutable/deterministic contracts; stdlib-only unless a driver is injected.

## Phase 10 milestones (from roadmap)

- [ ] **P10-A — Agent Observation Boundary**: agents receive scoped, evidence-aware observations rather than unrestricted graph mutation access;
- [ ] **P10-B — Tool / Action Boundary**: agent tools produce proposals or ExecutionCommands, never direct canonical mutations;
- [ ] **P10-C — Simulation-before-Execution**: material decisions can be evaluated against deterministic simulation/optimization before authorization;
- [ ] **P10-D — Policy-aware Autonomy**: confidence, risk, monetary impact, scope, and approval policy determine autonomy level;
- [ ] **P10-E — Human-in-the-loop Control**: explicit review, override, escalation, and delegation paths;
- [ ] **P10-F — Agent Replay / Audit**: every agent observation, proposal, decision, authorization, command, and outcome is replayable;
- [ ] **P10-G — Phase 10 acceptance**: a bounded SCM use case can autonomously observe -> reason -> simulate -> obtain authorization -> execute -> learn from outcome while remaining governed.

## Existing contracts Phase 10 builds on

Phase 10 composes the now-stable governed layer rather than inventing new
semantics. Key modules the slices extend:

- **Observation / reasoning (P10-A, P10-B)**: `graph_query.py`, `graph_projection.py`, `graph_reasoning_projection.py` (`GraphReasoningObservation`), `context_assembly.py`, `governed_reasoning_input.py`, `reasoning_input.py`, `reasoning_output.py`, `reasoning_assembly.py`, `reasoning_provider.py`, `rule_reasoning_provider.py`, `llm_reasoning_provider.py`, `auditable_reasoning.py`, `reasoning_gate.py`, `reasoning_policy.py`, `reasoning_output_governance.py`.
- **Simulation / optimization (P10-C)**: `governed_simulation.py` (S363), `optimized_planning.py` (S364), `optimized_app_planning.py` (S365), `simulation.py`, plus `docs/S363-governed-simulation.md`, `docs/S364-optimized-planning.md`, `docs/S365-optimized-app-planning.md`.
- **Authorization / governance (P10-D, P10-E)**: `decision_authorization.py`, `proposal_validation.py`, `governed_audit.py` (S354), `command_lifecycle.py` (S355), `authorization_governance.py` (S356), `constraint_policy.py`, `policy_expression.py`, `capability_negotiation.py`, `capability_aware_negotiation.py`, `canonical_capabilities.py`.
- **Execution / outcomes (P10-C..P10-G)**: `execution_command.py`, `execution_outcome_contract.py`, `external_execution_adapter.py`, `approval_to_execution_runtime.py`, `outcome_to_event_canonicalization.py`, `failure_retry_idempotency.py`, `closed_loop_e2e.py`.
- **Learning / feedback (P10-F, P10-G)**: `decision_learning.py`, `runtime_feedback.py`, `feedback_loop.py`, `learned_knowledge.py`, `learning_evidence.py`, `closed_loop_runtime.py`, `closed_loop_snapshot.py`.
- **Legacy second-loop contracts (reference)**: `closed_loop_runtime.py`, `decision_trace.py`, `execution_trace.py`, `end_to_end_accountability.py`, `auditable_reasoning.py`.

The S371 `closed_loop_runtime` and the P9 E2E already demonstrate a governed
loop; Phase 10 surrounds that loop with agent boundaries, autonomy policy, and
replayable agent audit.

## Recommended first slice

**P10-A — Agent Observation Boundary** is the natural small next milestone: a
scoped, evidence-aware `AgentObservation` bound that hands agents
`GraphReasoningObservation`-style reads while blocking unrestricted graph
mutation access. It extends the existing `graph_reasoning_projection.py` read
path without adding agent semantics to the ontology.

## Suggested workflow for a new session

1. `git checkout main && git pull` — inspect latest `main` and CI (Phase 9 is merged; verify `PYTHONPATH=src python -m scm_ontology.validator`).
2. `git status` / `gh pr list` — confirm no stale branches or open PRs.
3. Re-read `AGENTS.md`, `docs/roadmap-post-m8.md`, and this handoff.
4. Implement the chosen milestone following the repo loop: inspect -> model -> contract -> implement -> validate -> test -> document -> PR -> governed merge.
5. One PR per slice; update `POST-M8-STATUS.md`, the roadmap checklist, `docs/README.md`, and `README.md` with each slice.
6. Keep historical milestone documents intact; only correct them for genuine fact corrections.
7. Phase 10 is about **bounded autonomy inside the governed loop** — never broaden scope or weaken governance to make an agent path easier.
