# S353 — SCM Execution Runtime v0

## Purpose

S353 is the first **Execution Runtime** milestone (Phase R3). It processes an
immutable `ExecutionCommand` through a bounded, injected `ExecutionAdapter`
and produces an immutable `DryRunExecutionResult` describing what *would* be
executed. It performs no external side effects.

This milestone composes the canonical path end to end:

```text
observations -> ... -> ExecutionCommand -> Dry Run -> ExecutionResult
```

It reuses the S346 command contract and the S348 governed loop. It does not
define a new canonical semantic boundary.

## Contract

`execute_dry_run(command, *, dry_ran_at, adapter)` accepts an immutable
`ExecutionCommand` and an injected `ExecutionAdapter` (a bounded boundary that
MUST be deterministic and side-effect-free). It returns an immutable
`DryRunExecutionResult` containing:

- `command` — the original immutable command;
- `plan` — the planned `execution_target`, `action`, `payload`, and optional `detail`;
- `result_id` — deterministic hash of the serialized command and plan;
- `dry_ran_at` — caller-supplied timestamp;
- `status` — `"dry-run"`.

Evidence and provenance identifiers are preserved from the command. The result
serializes deterministically with `contract_version: S353.1`.

`run_governed_loop_and_dry_run(...)` composes the S348 governed loop with the
dry run and returns an immutable `GovernedExecutionResult`
(`contract_version: S353.2`).

## Fail-closed behavior

`execute_dry_run` MUST reject:

- a value that is not an `ExecutionCommand`;
- a missing or blank `dry_ran_at`;
- an adapter without a non-empty `adapter_id` or a callable `dry_run`;
- an adapter plan that is not a mapping or lacks a valid target/action.

An adapter failure is wrapped so the runtime stops rather than issuing a plan.

## Non-goals

S353 does not:

- call ERP, WMS, TMS, MES, or other external systems;
- mutate Canonical Truth, graph storage, or any external system;
- execute the command or commit an external write;
- infer authorization policy;
- persist or replay executions (Runtime Phase R4).
