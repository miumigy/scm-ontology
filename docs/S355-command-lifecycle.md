# S355 — Command Lifecycle

## Purpose

S355 is a Governance milestone (Phase R4). It adds an immutable, governed,
append-only state machine for a command so every step from proposal to
execution is explicit and recorded.

## Contract

`start_command_lifecycle(command_id)` places a command in the `proposed` state.

`transition_command(lifecycle, *, to_state, occurred_at, actor_id, reason)`
moves a command to a new state and records a `CommandTransition`. Allowed
transitions are:

```text
proposed -> authorized -> approved -> dry_run -> executing -> executed
proposed -> rejected
authorized -> rejected
proposed -> cancelled
approved -> cancelled
```

Terminal states (`executed`, `rejected`, `cancelled`) accept no further
transitions. Each transition records `occurred_at`, `actor_id`, and optional
`reason`, and is appended (immutably) to the lifecycle. A `CommandLifecycle` is
content-addressed and serializes deterministically with `contract_version:
S355.1`.

## Fail-closed behavior

The lifecycle MUST reject:

- blank command identifiers or transitions without a timestamp/actor;
- a transition not in the allowed set;
- any transition from a terminal state.

## Non-goals

S355 does not:

- mutate Canonical Truth or external systems;
- execute the command;
- infer authorization policy.
