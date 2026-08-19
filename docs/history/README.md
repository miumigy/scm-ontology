# Development History

This directory preserves the **sequential development history** of the SCM OS
reference build (Phases 6–10) as it was constructed toward the v0.1.0 Primary
Launch. It is **not** the current product surface.

For how to use the current product, start at the repository
[`README.md`](../../README.md) and the [`docs/launch/`](../launch/README.md)
Golden Path. For the semantic specification, see [`docs/semantics/`](../semantics/).
For the current architecture, see [`docs/architecture/`](../architecture/).

Each phase below is one directory with content-named files (e.g. phase number →
directory, capability → filename).

## Phase index

- [`phase6/`](phase6/) — SCM OS Control Plane (SCM OS Cockpit, Decision Inbox,
  Simulation/Optimization Workspace, Execution Workflow Workspace, Control Plane E2E, acceptance)
- [`phase7/`](phase7/) — SCM OS Real Data Plane (Reference Data Adapter, Mapping / Canonicalization
  Runtime, Identity Resolution Runtime, Data Quality / Freshness Gate, Multi-source Reference Dataset, acceptance)
- [`phase8/`](phase8/) — Persistent SCM Graph (Persistent Graph Contract, Relational Reference Backend,
  Neo4j Reference Backend, Snapshot / Version / Replay, Scale / Index Boundary, acceptance)
- [`phase9/`](phase9/) — Closed-Loop SCM OS Execution (Execution Outcome Contract, External Execution
  Adapter, Approval-to-Execution Runtime, Outcome-to-Event Canonicalization, Closed-Loop E2E,
  Failure / Retry / Idempotency, acceptance)
- [`phase10/`](phase10/) — Autonomous SCM Control (Agent Observation Boundary, Tool / Action Boundary,
  Simulation-before-Execution, Policy-aware Autonomy, Human-in-the-loop Control, Agent Replay / Audit, acceptance)

## Purpose

These records document **how** the SCM OS reference runtime was built phase by
phase. They are retained for provenance and traceability. They are not normative
contracts for the current product; the normative specification lives in
[`docs/semantics/`](../semantics/) and the launch surface in [`docs/launch/`](../launch/).
