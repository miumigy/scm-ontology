# S124 — Temporal SCM Graph

S124 projects the temporal semantics of S106 onto the graph model established by S123.

## Core rule

Time is semantic, not merely a timestamp property.

```text
Event != State
Effective Time != Transaction Time
Observation Time != Recording Time
Planned Time != Actual Time
```

## Temporal assertion

A graph assertion may carry distinct temporal dimensions:

- `valid_from` / `valid_to`: when a fact or state is valid in the modeled world;
- `transaction_time`: when the assertion was recorded or changed in the source system;
- `observation_time`: when the state/value was observed or measured;
- `planned_time`: intended future timing;
- `promised_time`: committed timing;
- `actual_time`: execution timing.

These dimensions must not be collapsed into a single `timestamp`.

## Event and state

An Event represents something that occurred or is asserted to occur at a point or interval.
A State represents a condition that is valid over an interval.

```text
Event
  └─ causes / results_in
       ↓
State Transition
       ↓
State(valid_from, valid_to)
```

A new state does not delete the previous state. Historical states remain reconstructable.

## Planned / promised / actual

The graph must preserve separate temporal assertions for planning and execution.

```text
Plan → planned_time
Commitment → promised_time
Execution → actual_time
```

An actual event does not rewrite the original plan or commitment.

## Reconstruction

For a requested world-time `t`, state reconstruction selects assertions whose validity interval contains `t`, subject to the relevant scenario and identity resolution.

For an as-recorded view, transaction time is additionally constrained. This allows questions such as:

- What was true at time T?
- What did the system know at time T?
- What was planned at time T?
- What was actually executed?

## Scenario boundary

Temporal history and scenario projections remain distinct. A counterfactual state must not be inserted into Actual history merely because its validity interval resembles an actual state interval.

## Provenance boundary

Every temporal assertion should remain traceable to its source/provenance where available. Restatement is represented as a new assertion/version, not silent mutation of historical truth.

## Non-goals

S124 does not define a graph database implementation, temporal indexing strategy, or query language. Those are implementation concerns above the canonical temporal semantics.
