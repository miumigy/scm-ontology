# P9-E — Closed-Loop SCM OS Execution E2E

## Purpose

P9-E composes the Phase 9 slices into one deterministic closed loop that starts
from operational state and lands back on updated state:

```text
State -> Decision -> Authorization -> Execution -> Outcome
     -> Canonical Event -> Updated State
```

It binds together the S348 governed decision loop, the P9-C
approval-to-execution runtime, the P9-B external execution adapter, and the P9-D
outcome-to-event canonicalization.

The operative `ClosedLoopState` is an explicit, **derived** operational snapshot
(`derived = True`). Applying an outcome updates that derived state only; it never
mutates Canonical Truth directly — every outcome effect flows through the
governed execution/event boundary first (per AGENTS.md, rules 10 & 12).

## Contract

`src/scm_ontology/closed_loop_e2e.py`:

- **`ClosedLoopState`** — immutable derived operational snapshot (`on_hand`,
  `open_purchase_orders`, `reorder_point`, `reorder_quantity`), permanently
  labelled `derived = True`.
- **`ReplenishmentRuleProvider`** — deterministic rule provider that proposes a
  `replenish` operation when `on_hand < reorder_point`, else `no_operation`.
- **`run_closed_loop_e2e(...)`** — run one iteration and return an immutable
  `ClosedLoopE2EResult`.
- **`ClosedLoopE2EResult`** — the decision, approval/execution, canonical event,
  `state_before`, `state_after`, and an `executed` flag.

### Loop behaviors

| proposal | execution | canonical event | state after |
|---|---|---|---|
| `replenish` (stock low) | governed external execution | `execution_outcome_recorded` | succeeded portion applied |
| `no_operation` (stock ok) | none | none | unchanged |

A `failure` outcome leaves the derived state unchanged (the side effect did not
complete); a `partial` outcome applies the succeeded portion.

## Fail-closed behavior

- State quantities must be non-negative; the state must remain explicitly derived.
- `context_id`, `actor_id`, and `authority` must be non-empty.
- `no_operation` decisions never reach the external adapter (no side effect).

## Guardrails

- Canonical events are produced only through the governed path (P9-D), which
  requires the executed lifecycle state.
- The updated state is a derived projection, explicitly distinguished from
  Canonical Truth.
