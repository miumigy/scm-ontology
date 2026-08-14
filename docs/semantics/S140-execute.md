# S140 — Execute

S140 defines the SCM OS Execute semantic: turning an authorized decision and intended action into an execution record while preserving the distinction between intent, execution, and actual outcome.

## Execute contract

```text
Decision
   ↓ authorizes / establishes
Action
   ↓ initiated
Execution
   ↓ produces evidence
Actual Outcome / State Change
```

Execution records what was carried out, not merely what was decided or intended.

## Core boundaries

- Decision ≠ Action
- Action ≠ Execution
- Execution ≠ Outcome
- Planned ≠ Actual
- Intended ≠ Executed
- Executed ≠ Successfully completed
- Execution ≠ Event
- State Change ≠ Execution

An execution may be partial, failed, cancelled, interrupted, or completed.

## Action context

An Action expresses an intended operational intervention. It may reference the Decision that authorized it, the Plan it implements, target subjects, intended quantities, timing, and applicable constraints.

## Execution context

An Execution should preserve, where applicable:

- action reference
- executor / executing actor
- execution start and end time
- execution status
- actual quantities or values
- execution location / resource
- event references
- resulting state-change references
- exception / failure references
- provenance

## Execution status

Execution status is explicit and does not imply outcome success:

- pending
- started
- in_progress
- partially_completed
- completed
- failed
- cancelled
- interrupted

A `completed` execution means the execution process reached completion; it does not by itself prove that the intended business outcome was achieved.

## Partial execution

One Action may produce multiple Executions or partial execution records. Actual execution quantity must not overwrite the originally intended quantity.

```text
Action: ship 100 units
   ↓
Execution 1: 60 units
Execution 2: 40 units
```

## Actual outcome and state

Execution may produce evidence of an actual outcome or state transition. The resulting Actual is represented separately so that execution itself is not mistaken for what happened in the physical or business world.

## Temporal semantics

Execution time is distinct from decision time, planned time, scheduled time, promised time, and transaction/recording time. Historical execution records remain immutable in meaning even when later corrections or restatements occur.

## Scenario execution

Execution in a Scenario or simulation is not an actual-world execution. Scenario execution remains scoped to its scenario unless explicitly materialized into the actual world through a separate authoritative process.

## Failure and exception

An execution can fail without the Action becoming invalid. Failure is an execution result and may trigger a new Diagnosis, Decision, or Action.

```text
Execute
  ↓
Failure / Exception
  ↓
Observe → Diagnose → Decide → Execute
```

## Non-goals

S140 does not define workflow engines, robotics protocols, transportation execution systems, MES interfaces, or task scheduling algorithms. It defines the canonical semantics of execution independent of implementation technology.
