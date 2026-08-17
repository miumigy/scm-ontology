# S364 — Optimized Replenishment Plan Application

## Purpose

S364 is the **planning/optimization integration** milestone (Phase 5). It
extends the single-period replenishment decision (S358) into a **multi-period,
cost-aware replenishment plan** that is optimized deterministically and then
executed period-by-period through the governed loop.

It composes existing boundaries without introducing new canonical
semantics:

- `s138_plan.Plan` (and `create_plan`) to represent the plan as a first-class
  artifact with objectives, constraints, and provenance;
- the `planning_boundary` concept, surfaced as explicit plan metadata
  (objective and constraint refs) carried by the `Plan`, keeping the
  optimizer->planner boundary declarative;
- the S348 golden loop + S358 replenishment application to turn each period's
  optimized replenishment into an authorized `ExecutionCommand` and S353 dry
  run.

## Contract

`run_optimized_planning(observation, *, context_id, actor_id, authority,
authorized_at, command_id_prefix, dry_ran_at, adapter)` accepts an
`OptimizedReplenishmentObservation` and returns an immutable
`OptimizedPlanningResult` with `contract_version: S364.1`.

`OptimizedReplenishmentObservation` carries one product/location scope over a
fixed number of periods:

- `product_id`, `location_id`, `unit`;
- `initial_on_hand` (starting inventory);
- `demands` (one non-negative quantity per period, length N);
- `replenishment_cost` and `holding_cost` per unit (non-negative);
- `reorder_point` (period-level replenishment threshold);
- `evidence_ids`, `provenance_ids`.

The optimizer deterministically computes, for each period, the smallest
replenishment quantity that avoids a stockout (or, when a batch is ordered,
the minimum batch that covers the projected shortfall), minimizing total
`replenishment_cost + holding_cost` over the horizon. The resulting per-period
decisions are recorded in a `Plan` (`plan_type="replenishment_plan"`) and each
is executed through the governed loop with a distinct `command_id`.

## Fail-closed behavior

The application MUST reject:

* empty product/location/unit or missing context;
* non-numeric or negative costs / batch / point;
* empty demands or a negative demand quantity;
* mismatched input types (not an `OptimizedReplenishmentObservation`);
* non-positive horizon (no periods).

A period whose optimized replenishment is zero is recorded as a `no_action`
replenishment (no command). A period that requires a replenishment produces an
authorized command and dry run.

## Non-goals

S364 does not:

- mutate Canonical Truth or external systems;
- infer demand or forecast (demands are supplied as observations);
- execute any command (dry run only);
- allocate across multiple products/locations (single scope);
- introduce new canonical Entity or Relationship types.
