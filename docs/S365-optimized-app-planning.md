# S365 — Optimized Procurement, Production & Distribution Planning

## Purpose

S365 is the **planning/optimization integration** milestone (Phase 5) for the
remaining R5 applications. It extends the single-period procurement (S360),
production (S361), and distribution (S362) decisions into **multi-period,
optimized plans** that are computed deterministically and then executed
period-by-period through the governed loop.

S364 covered replenishment (S358). S365 applies the same pattern to the other
three R5 applications, so the Phase 5 planning/optimization integration spans
the full physical material flow: replenish -> procure -> produce -> distribute.

S365 introduces **no new canonical semantics** and performs **no external side
effect**. It reuses the S348 governed loop, the S351 rule-based provider, the
S353 execution runtime, the `Plan` / `create_plan` boundary, and the R5
application runners.

## Contract

Each optimized application is exposed as a bounded, deterministic function over
a multi-period observation:

- `run_optimized_procurement_planning(observation, *, context_id, actor_id,
  authority, authorized_at, command_id_prefix, dry_ran_at, adapter)` accepts an
  `OptimizedProcurementObservation` (item, per-period shortages, supplier) and
  returns an immutable `OptimizedProcurementResult` with `contract_version:
  S365.1`.

- `run_optimized_production_planning(observation, *, ...)` accepts an
  `OptimizedProductionObservation` (resource, per-period requirements,
  capacity) and returns an immutable `OptimizedProductionResult`.

- `run_optimized_distribution_planning(observation, *, ...)` accepts an
  `OptimizedDistributionObservation` (shipment id, item, per-period required
  quantities, capacity, origin, destination) and returns an immutable
  `OptimizedDistributionResult`.

Each optimizer computes the deterministic per-period action:

- **Procurement**: procure the projected shortage in each period; a zero
  shortage yields `no_procurement` with no command.
- **Production**: schedule the required quantity in each period when it is
  within capacity; an over-capacity requirement yields `escalate`.
- **Distribution**: ship the required quantity in each period when it is within
  capacity; an over-capacity requirement yields `escalate`.

Every result records a `Plan` (`plan_type` set to `procurement_plan`,
`production_plan`, or `distribution_plan`) and per-period governed decisions.

## Fail-closed behavior

Each application MUST reject:

- empty identifiers (item/resource/shipment/origin/destination) or missing
  context;
- empty or non-numeric per-period tuples;
- negative quantities or capacities;
- mismatched input types;
- a non-positive horizon (no periods).

A period that requires no action is recorded as `no_action` with no command.

## Non-goals

S365 does not:

- mutate Canonical Truth or external systems;
- infer demand or forecast (demands are supplied as observations);
- execute any command (dry run only);
- allocate across multiple resources/routes (single scope per run);
- introduce new canonical Entity or Relationship types.
