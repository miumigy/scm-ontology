# S358 — Replenishment Decision Application

## Purpose

S358 is the first **SCM Application** milestone (Phase R5). It puts the
governed decision loop to work for a concrete business problem: resolving
on-hand inventory to a replenishment decision and, when a reorder is required,
driving that decision through the S348 governed loop to an authorized
`ExecutionCommand` and an S353 dry run.

It is a vertical Application-Layer slice. It reuses the S326 inventory
observation semantics, the S351 rule-based provider, the S348 decision runtime,
and the S353 execution runtime. It introduces no new canonical semantics and
performs no external side effect.

## Contract

`run_replenishment_application(observation, *, context_id, actor_id, authority,
authorized_at, command_id, dry_ran_at, adapter)` accepts a
`ReplenishmentObservation` (product, location, on-hand, reorder point, reorder
quantity, unit, evidence, provenance) and returns an immutable
`ReplenishmentDecision` with `contract_version: S358.1`.

When on-hand is **at or above** the reorder point, the application returns a
`no_replenishment` decision with no command and no dry run. When on-hand is
**below** the reorder point, it builds a deterministic rule provider
(`replenish-below-reorder-point`) and runs the full governed loop:

```text
observation -> ReasoningInput -> Rule provider -> ReasoningOutput
    -> Validation -> Authorization -> ExecutionCommand -> Dry Run -> Result
```

The decision records the proposed `action` and `quantity` and, for a
replenishment, bundles the governed result (`GovernedExecutionResult`) for
audit.

## Fail-closed behavior

The application MUST reject:

- empty product/location/unit or missing context;
- non-numeric quantities;
- invalids inputs (a value that is not a `ReplenishmentObservation`).

It returns `no_replenishment` without creating a command when no reorder is
needed, rather than generating an unnecessary side effect.

## Non-goals

S358 does not:

- mutate Canonical Truth or external systems;
- reserve or allocate inventory;
- perform sourcing, procurement, or transportation planning;
- infer demand or forecast;
- execute the command.
