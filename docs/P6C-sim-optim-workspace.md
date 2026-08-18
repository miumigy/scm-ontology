# P6-C — Simulation / Optimization Workspace

## Purpose

P6-C is the third **Phase 6 (SCM OS Control Plane)** slice. It provides a
**Simulation / Optimization Workspace**: a single surface to **launch and
inspect deterministic scenarios and plans** from the control plane.

P6-C composes the existing governed contracts:

- governed simulation (S363) → **scenarios**;
- optimized replenishment planning (S364) → **plans**;
- optimized procurement / production / distribution planning (S365) → **plans**.

It projects each launched artifact into an immutable, deterministic, JSON-safe
`WorkspaceScenario` / `WorkspacePlan` and folds them into a content-addressed
`WorkspaceState` with a workspace summary. It never re-derives or mutates a
scenario/plan and performs no external side effect.

## Contract

`launch_simulation(...)` composes `run_governed_simulation` and returns a
`WorkspaceScenario`; `launch_replenishment_plan` / `launch_procurement_plan` /
`launch_production_plan` / `launch_distribution_plan` compose the corresponding
optimized-planning launchers (S364/S365) and return a `WorkspacePlan`.

`workspace_scenario(result, *, created_at)` / `workspace_plan(result, *,
application=None, created_at)` project already-produced results read-only (no
recomputation).

`build_workspace_state(*, scenarios, plans, created_at, view_actor_id)` returns
an immutable `WorkspaceState` with `contract_version: P6C.1` and
`is_workspace: true`:

| projection | fields |
|---|---|
| `WorkspaceScenario` | `scenario_id`, `context_id`, step counts, `actionable/no_action` steps |
| `WorkspacePlan` | `plan_ref`, `plan_type`, `status`, `application`, `period_count`, `total_quantity`, `source_contract_version` |
| `WorkspaceState` | content-addressed `workspace_id` + `WorkspaceSummary` (scenario/plan/step/period counts) |

`launch_reference_workspace()` is the deterministic reference path: one
scenario plus the four optimized plans across the physical material flow
(replenish → procure → produce → distribute).

## Fail-closed behavior

The workspace MUST reject:

- a workspace with no scenario and no plan, duplicate scenario ids or plan refs;
- a `scenario`/`plan` entry of the wrong type or a non-`WorkspaceScenario`/`WorkspacePlan`;
- missing `created_at` / `view_actor_id` or a blank scenario/plan identity/scope;
- a plan artifact that is not one of the signed optimized-plan results.

## Determinism & provenance

- The same launched inputs and timestamps produce an identical workspace
  (`to_json`) and content-addressed `workspace_id`.
- Inspection is read-only: building a `WorkspaceState` re-derives no scenario
  and re-executes no plan.

## Non-goals

P6-C does not:

- re-run or re-optimize any launched scenario/plan for inspection;
- mutate Canonical Truth or external systems;
- persist a workspace (in-memory projection only);
- introduce new canonical Entity, Relationship, or derived-state types.
