# S360 — Procurement Decision Application

## Purpose

S360 is an **SCM Application** milestone (Phase R5). It resolves a demand/supply
shortage into a procurement decision and, when a purchase is required, drives it
through the governed loop to an authorized `ExecutionCommand` and an S353 dry
run.

It reuses the S348 governed loop, the S351 rule-based provider, and the S353
execution runtime. It introduces no new canonical semantics and performs no
external side effect.

## Contract

`run_procurement_application(observation, *, context_id, actor_id, authority,
authorized_at, command_id, dry_ran_at, adapter)` accepts a
`ProcurementObservation` (item, shortage, unit, supplier, evidence, provenance)
and returns an immutable `ProcurementDecision` with
`contract_version: S360.1`.

When the shortage is non-positive, the application returns a
`no_procurement` decision with no command and no dry run. When a shortage
exists, it builds a deterministic rule provider (`procure-on-shortage`) and
runs the full governed loop:

```text
observation -> ReasoningInput -> Rule provider -> ReasoningOutput
    -> Validation -> Authorization -> ExecutionCommand -> Dry Run -> Result
```

## Fail-closed behavior

The application MUST reject:

- empty item/unit or missing context;
- non-numeric or negative shortage;
- a value that is not a `ProcurementObservation`.

It returns `no_procurement` without creating a command when there is no
shortage.

## Non-goals

S360 does not:

- mutate Canonical Truth or external systems;
- place the purchase order or release funds;
- negotiate pricing or supplier selection beyond the supplied `supplier_id`;
- infer demand or forecast;
- execute the command.
