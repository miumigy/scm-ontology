# P9-C — Approval-to-Execution Runtime

## Purpose

P9-C advances a governed command from its approved dry-run state to a
**controlled external execution** and captures the immutable P9-A
outcome contract. It composes:

- the S355 command lifecycle (which already reaches the `dry_run` state);
- the S354 governed audit;
- the P9-B external execution adapter boundary;
- the P9-A execution outcome contract.

It enforces a fail-closed gate: a command may only be executed once it has been
authorized, approved, and dry-run, and only through an injected external
adapter. It performs no canonical mutation and records every transition with an
actor.

## Contract

`src/scm_ontology/approval_to_execution_runtime.py`:

- **`build_approved_lifecycle(command_id, *, recorded_at, actor_id)`** — build a
  lifecycle advanced to the `approved` state (proposed → authorized → approved).
- **`approve_and_execute(command, *, adapter, executed_at, actor_id[, external_system, lifecycle, dry_run])`** —
  progress the command from its approved dry-run state through
  `dry_run → executing → executed`, executing through the P9-B adapter, and
  return an immutable `ApprovalToExecutionResult`.
- **`ApprovalToExecutionResult`** — the recorded `lifecycle` (at the terminal
  `executed` state), the `dry_run`, the immutable `outcome`, and `executed_at`.

### State flow

```text
proposed -> authorized -> approved -> dry_run -> executing -> executed
```

If no lifecycle/dry-run is supplied, the runtime builds the approved lifecycle
and computes the dry run for you; otherwise it fails closed unless the lifecycle
is already at `dry_run`.

## Fail-closed behavior

- A command may not be executed unless its lifecycle is at `dry_run` (an earlier
  state, or a terminal state, is refused).
- The dry run is computed with the standard S353 in-process dry-run adapter —
  never by the external side-effect adapter (which by contract performs real
  side effects and is only used at the execute gate).
- The external adapter must pass P9-B validation and support the command type.
- Every lifecycle transition must be in the S355 allowed-transition set; an
  out-of-order or unauthorized transition is refused.

## Guardrails

- Execution through the external adapter is a real side effect, but the outcome
  is only recorded as an immutable P9-A contract — never a canonical mutation.
- All state transitions are carried by the append-only, content-addressed
  lifecycle and audit structures.
