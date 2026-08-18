# S366 — Operational Workflow Application

## Purpose

S366 is the **visualization & operational workflow integration** milestone
(Phase 5). It takes the governed decision output produced by the R5/Phase 5
applications (replenishment S358, procurement S360, production S361,
distribution S362 — and their multi-period optimizations S364/S365) and turns
it into an **operational workflow**: each governed decision is audited,
tracked through its command lifecycle, and folded into a deterministic
workflow report.

S366 closes the loop after a decision is made: it does not re-derive the
decision. It reuses the S348 governed loop output (`GovernedExecutionResult`),
the S354 governed-audit boundary, and the S355 command-lifecycle state
machine. It introduces **no new canonical semantics** and performs **no
external side effect**.

## Contract

`run_operational_workflow(steps, *, workflow_id, recorded_at)` accepts an
ordered sequence of `OperationalStep` values and returns an immutable
`OperationalWorkflowResult` with `contract_version: S366.1`.

Each `OperationalStep` binds one existing governed decision to its workflow
step:

- `step_id`, `application` (one of the R5 application names);
- `decision`: the immutable R5 decision object (a `ReplenishmentDecision`,
  `ProcurementDecision`, `ProductionDecision`, or `DistributionDecision`);
- `command_id` for the generated execution command.

For each step the application:

1. reads the governed result (`decision.governed`) present on the decision;
2. when a governed result exists, records a content-addressed audit entry via
   the S354 boundary (`record_governed_decision`) and starts the command
   lifecycle via S355 (`start_command_lifecycle`), advancing it through the
   dry-run state (authorized -> approved -> dry-run);
3. when the decision is a `no_action` (no governed result), records the step as
   `no_action` with no command and no lifecycle;
4. folds every step into an immutable workflow report (state, audit id, command
   id) plus a workflow-level summary.

## Fail-closed behavior

The application MUST reject:

- an empty or non-iterable step sequence;
- a step whose `decision` is not one of the supported R5 decision types;
- a step whose `application` does not match the decision type;
- missing `step_id`, `application`, `command_id`, `workflow_id`, or
  `recorded_at`;
- duplicate step ids within the workflow.

## Determinism & provenance

- The same ordered steps, `workflow_id`, and `recorded_at` produce identical
  workflow report and per-step audit/lifecycle ids.
- The report is immutable and JSON-safe (`to_mapping` / `to_json`).
- Audit entries and lifecycle transitions are deterministic and replayable.

## Non-goals

S366 does not:

- re-derive or re-compute any decision (it consumes governed outputs);
- mutate Canonical Truth or external systems;
- execute any command (dry run only);
- persist to a store (in-memory report only);
- introduce new canonical Entity or Relationship types.
