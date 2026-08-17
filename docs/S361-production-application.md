# S361 — Production Decision Application

## Purpose

S361 is an **SCM Application** milestone (Phase R5). It resolves a production
requirement against resource capacity into a scheduling decision and, when
production is feasible, drives it through the governed loop to an authorized
`ExecutionCommand` and an S353 dry run.

It reuses the S348 governed loop, the S351 rule-based provider, and the S353
execution runtime. It introduces no new canonical semantics and performs no
external side effect.

## Contract

`run_production_application(observation, *, context_id, actor_id, authority,
authorized_at, command_id, dry_ran_at, adapter)` accepts a
`ProductionObservation` (resource, required, capacity, unit, evidence,
provenance) and returns an immutable `ProductionDecision` with
contract_version: S361.1.

When the requirement **exceeds** capacity (infeasible), the application returns
an `escalate` decision with no command and no dry run. When the requirement is
within capacity (feasible, including exact fit), it builds a deterministic rule
provider (`schedule-feasible-production`) and runs the full governed loop:

```text
observation -> ReasoningInput -> Rule provider -> ReasoningOutput
    -> Validation -> Authorization -> Command -> Dry Run -> Result
```

## Fail-closed behavior

The application MUST reject:

- empty resource/unit or missing context;
- non-numeric or negative required/capacity;
- a value that is not a `ProductionObservation`.

It returns `escalate` without creating a command when the requirement is not
feasible.

## Non-goals

S361 does not:

- mutate Canonical Truth or external systems;
- schedule or dispatch to a shop floor / MES;
- allocate materials or labor;
- optimize the production plan;
- execute the command.
