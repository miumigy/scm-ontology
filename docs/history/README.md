# Development History

This directory is the **development archive** for SCM Ontology. It preserves
*how* the project was designed and built — the milestones, the post-M8
implementation roadmap, and the sequential SCM OS reference build (Phases 5–10).
It is **not** the current product surface and is not required reading for a
v0.1.0 user.

For how to use the current product, start at the repository
[`README.md`](../../README.md) and the [`docs/launch/`](../launch/README.md)
Golden Path. For the normative semantic specification, see
[`docs/semantics/`](../semantics/). For the current architecture, see
[`docs/architecture/`](../architecture/).

## Orientation

- [`milestones-status.md`](milestones-status.md) — milestone status archive
  (M1–M8 definitions and acceptance summaries)
- [`post-m8-roadmap.md`](post-m8-roadmap.md) — the post-M8 roadmap that drove
  Phases 5–10 (now completed)
- [`post-m8/`](post-m8/) — earlier post-M8 architecture planning notes that
  were superseded by the Phase 8 persistent-graph implementation

## Legacy archive

- [`legacy/`](legacy/) — superseded early-design documents (S1–S7 simulation/
  causal, S116 schema note, M6 fixture note, M4 freeze, v0.2 RC) retained for
  provenance only

## Phase index

Each phase is one directory with content-named files.

- [`phase5/`](phase5/) — M5 SCM use-case validation (and M5/M6 acceptance history)
- [`phase6/`](phase6/) — SCM OS Control Plane (SCM OS Cockpit, Decision Inbox,
  Simulation/Optimization Workspace, Execution Workflow Workspace, Control Plane E2E, acceptance)
- [`phase7/`](phase7/) — SCM OS Real Data Plane (Reference Data Adapter, Mapping / Canonicalization
  Runtime, Identity Resolution Runtime, Data Quality / Freshness Gate, Multi-source Reference Dataset, acceptance)
- [`phase8/`](phase8/) — Persistent SCM Graph (Persistent Graph Contract, Relational Reference Backend,
  Neo4j Reference Backend, Snapshot / Version / Replay, Scale / Index Boundary, M8 acceptance, acceptance)
- [`phase9/`](phase9/) — Closed-Loop SCM OS Execution (Execution Outcome Contract, External Execution
  Adapter, Approval-to-Execution Runtime, Outcome-to-Event Canonicalization, Closed-Loop E2E,
  Failure / Retry / Idempotency, acceptance)
- [`phase10/`](phase10/) — Autonomous SCM Control (Agent Observation Boundary, Tool / Action Boundary,
  Simulation-before-Execution, Policy-aware Autonomy, Human-in-the-loop Control, Agent Replay / Audit, acceptance)

> Milestone and slice contracts (the historical `M5`–`M8` / `Sxxx` sequence)
> are archived under the matching phase directory above. They remain for
> provenance and traceability only.

## Purpose

These records document *how* the SCM OS reference runtime was built phase by
phase. They are retained for provenance and traceability. They are not
normative contracts for the current product; the normative specification lives
in [`docs/semantics/`](../semantics/) and the launch surface in
[`docs/launch/`](../launch/).
