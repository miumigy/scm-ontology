# P6-F — Phase 6 Acceptance

## Purpose

P6-F closes **Phase 6 (SCM OS Control Plane)** with a deterministic acceptance
contract. It verifies that the **major existing runtime capabilities are
discoverable and operable from one coherent SCM OS surface**.

P6-F defines an explicit Phase 6 capability inventory, probes each capability
deterministically (composing the P6-A..P6-E entry points plus the underlying
governed R5 application), and folds the results into an immutable,
content-addressed `Phase6AcceptanceReport` with an overall `accepted` flag.

## Capability inventory

| key | capability | entry point |
|---|---|---|
| `cockpit` | SCM OS Cockpit v0 (P6-A) | `run_cockpit_reference_path` |
| `governed_application` | Governed replenishment application (S358) | `run_replenishment_application` |
| `decision_inbox` | Decision Inbox (P6-B) | `build_decision_inbox` |
| `simulation_optimization_workspace` | Simulation/Optimization Workspace (P6-C) | `launch_reference_workspace` |
| `execution_workspace` | Execution Workflow Workspace (P6-D) | `launch_execution_workflow` |
| `control_plane_e2e` | Control Plane E2E (P6-E) | `run_control_plane_flow` |

## Contract

`run_phase6_acceptance(*, accepted_at)` returns an immutable
`Phase6AcceptanceReport` with `contract_version: P6F.1` and
`is_phase6_acceptance: true`.

Each capability is probed deterministically with reference inputs:

- **operable** — the probe returns a usable result without error; the output is
  fingerprinted into a content-addressed `evidence_id` (64 hex chars);
- **not operable** — the probe returned `None`/`False` or raised; the failure is
  recorded in `error` with a `CapabilityResult`.

A `CapabilityResult` exposes `key`, `name`, `operable`, `evidence_id`, and an
optional `error`. The report aggregates into an `AcceptanceSummary`
(capability/operable/failed counts) and sets:

- `accepted` — true only when every capability is operable;

and carries a content-addressed `report_id`.

## Fail-closed behavior

- A blank `accepted_at` is rejected.
- A capability probe that raises or returns no usable output is recorded as
  **not operable** (the probe never throws out of the acceptance run).

## Determinism & provenance

- The same probe inputs and `accepted_at` produce an identical report (`to_json`)
  and content-addressed `report_id`.
- Each operable capability is backed by an `evidence_id` fingerprint for replay.
- P6-F composes the existing P6-A..P6-E entry points. It re-derives no decision,
  mutates no Canonical Truth, and performs no external side effect.

## Non-goals

P6-F does not:

- execute or re-run any command;
- mutate Canonical Truth or external systems;
- persist the report (in-memory projection only);
- introduce new canonical Entity, Relationship, or derived-state types.
