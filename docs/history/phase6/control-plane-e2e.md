# P6-E — Control Plane E2E

## Purpose

P6-E is the fifth **Phase 6 (SCM OS Control Plane)** slice. It provides **one
deterministic user workflow** that traverses the full governed control-plane
chain

```text
State -> Decision -> Simulation/Plan -> Authorization -> Workflow -> Audit
```

and then composes the P6-A..P6-D control-plane surfaces over the produced
artifacts. P6-E is the Phase 6 acceptance slice: the major existing runtime
capabilities become operable from one coherent SCM OS surface.

## Contract

`run_control_plane_flow(request)` accepts a `ControlPlaneRequest` (`context_id`,
`operator_id`, `authority`, `observed_at`) and returns an immutable
`ControlPlaneE2EResult` with `contract_version: P6E.1` and
`is_control_plane_e2e: true`.

The flow composes the existing governed contracts end to end:

| stage | contract |
|---|---|
| `state` | demand/supply gap (canonical exception) |
| `decision` | replenishment application (S358) |
| `simulation_plan` | governed simulation (S363) + optimized replenishment plan (S364) |
| `authorization` | governed authorized decision (S345/S348) |
| `workflow` | operational workflow (S366) |
| `audit` | content-addressed governed audit entries (S354) |

The result then composes the four P6-A..P6-D control-plane surfaces:

- `cockpit` — P6-A `CockpitState` over state/exceptions/decisions/simulation/execution/governance;
- `decision_inbox` — P6-B `DecisionInbox` over the produced decision;
- `sim_optim_workspace` — P6-C `WorkspaceState` (scenario + plan);
- `execution_workspace` — P6-D `ExecutionWorkspace` (lifecycle, dry-run, audit).

A `ControlPlaneE2ESummary` aggregates per-stage counts; the result carries a
content-addressed `run_id`.

## Fail-closed behavior

P6-E MUST reject:

- a `ControlPlaneRequest` with blank `context_id` / `operator_id` / `authority` /
  `observed_at`;
- a flow invoked on a non-`ControlPlaneRequest`;
- a stage with an unknown name;
- a decision that produces no governed result (the chain cannot proceed).

## Determinism & provenance

- The same request produces an identical result (`to_json`) and content-addressed
  `run_id`.
- The flow re-derives no decision and performs no external side effect.
- The produced surfaces are read-only projections; the result is immutable and
  JSON-safe.

## Non-goals

P6-E does not:

- re-derive, re-run, or re-audit any decision it orchestrates;
- mutate Canonical Truth or external systems;
- persist the result (in-memory projection only);
- introduce new canonical Entity, Relationship, or derived-state types.
