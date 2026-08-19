# P6-D — Execution Workflow Workspace

## Purpose

P6-D is the fourth **Phase 6 (SCM OS Control Plane)** slice. It provides an
**Execution Workflow Workspace**: an operator-facing surface to **inspect
command lifecycle, dry-run results, approval gates, and audit trail** for
governed executions, without re-running or executing any command.

P6-D composes the existing governed execution contracts:

- command lifecycle (S355) → lifecycle state and recorded transitions;
- dry-run results (S353) → dry-run status / result id;
- governed audit (S354) → audit id;
- authorization / approval (S356) → approval-gate status.

## Contract

`CommandExecution` binds one governed execution from its already-produced
artifacts: a `CommandLifecycle` (required) plus optional `DryRunExecutionResult`,
`GovernedDecisionAuditEntry`, and `AuthorizationDecision`. It fails closed on
mismatched command ids or wrong artifact types.

`workspace_execution(lifecycle, *, command_type, dry_run=None, audit=None,
authorization=None)` projects an already-produced execution read-only into an
`ExecutionStep`; `build_execution_workspace(commands, *, created_at,
view_actor_id)` folds them into an immutable `ExecutionWorkspace` with
`contract_version: P6D.1` and `is_execution_workspace: true`.

Each `ExecutionStep` exposes:

| field | source |
|---|---|
| `state`, `is_terminal`, `transitions` | `CommandLifecycle` (S355) |
| `dry_run_status`, `dry_run_result_id` | `DryRunExecutionResult` (S353) |
| `audit_id` | `GovernedDecisionAuditEntry` (S354) |
| `approval` | derived from lifecycle + `AuthorizationDecision`: `approved` / `pending` / `denied` |

`launch_execution_workflow(*, governed_runs, actor_id, recorded_at, ...)` is the
deterministic reference path: for each `GovernedExecutionResult` (S353) it
advances the command lifecycle through the dry-run state (S355) and folds in the
dry-run result (S353) and governed audit entry (S354). It never re-derives any
decision.

## Fail-closed behavior

The workspace MUST reject:

- an empty or duplicate command sequence;
- a `CommandExecution` whose `lifecycle.command_id` does not match `command_id`;
- a wrong-type `dry_run` / `audit` / `authorization`;
- a non-`CommandExecution` entry or a non-`GovernedExecutionResult` run;
- blank `created_at` / `view_actor_id`.

## Determinism & provenance

- The same composed commands and timestamps produce an identical workspace
  (`to_json`) and content-addressed `workspace_id`.
- Inspection is read-only: building a workspace re-executes no command and
  re-derives no decision.

## Non-goals

P6-D does not:

- execute or re-run any command;
- mutate Canonical Truth or external systems;
- persist a workspace (in-memory projection only);
- introduce new canonical Entity, Relationship, or derived-state types.
