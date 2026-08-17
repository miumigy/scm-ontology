# S363 — Governed Simulation Application

## Purpose

S363 is the first **Phase 5 (SCM OS integration)** milestone. It composes the
existing Phase R5 governed applications (replenishment S358, procurement S360,
production S361, distribution S362) into a **multi-period, multi-decision
simulation** that runs each decision through the S348 governed loop.

A simulation is a bounded sequence of governed decisions executed against a
shared context. It demonstrates the operational workflow: each R5 observation
produces an authorized `ExecutionCommand` and an S353 dry run, and all steps
are recorded in an immutable, deterministic, side-effect-free run.

S363 introduces **no new canonical semantics** and performs **no external side
effect**. It reuses the S348 governed loop, the S351 rule-based provider, and
the S353 execution runtime. It preserves the M8 boundary between derived
decisions and Canonical Truth.

## Contract

`run_governed_simulation(steps, *, context_id, actor_id, authority,
authorized_at, command_id_prefix, dry_ran_at, adapter)` accepts an ordered
sequence of `SimulationStep` values and returns an immutable
`GovernedSimulationResult` with `contract_version: S363.1`.

Each `SimulationStep` binds one R5 decision application (replenishment,
procurement, production, or distribution) to its observation and a unique
command id:

```text
step -> observation -> governed loop -> decision + dry run  (per step)
```

A simulation step that requires no action (no reorder, no shortage, infeasible
capacity) is recorded as a `no_action` decision with no command, and the
simulation continues to the next step.

## Fail-closed behavior

The application MUST reject:

- an empty or non-iterable step sequence;
- a step whose application is not one of the supported R5 applications;
- a step whose observation is not a valid R5 observation for its application;
- missing context, actor, authority, or blank timestamps;
- duplicate step ids within the simulation.

A simulation step MUST fail the whole run if its governed loop raises, rather
than silently skipping or weakening validation.

## Determinism & provenance

- The same ordered step sequence, context, and timestamps produce identical
  simulation run id and step decision ids.
- Each step's decision preserves its observation evidence and provenance.
- The final result is immutable and JSON-safe (`to_mapping`).

## Non-goals

S363 does not:

- mutate Canonical Truth or external systems;
- optimize or allocate resources across steps;
- infer demand or forecast;
- execute any command (dry run only);
- introduce new R5 application types beyond the existing four.
