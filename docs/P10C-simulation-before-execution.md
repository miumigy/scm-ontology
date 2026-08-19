# P10-C — Simulation-before-Execution

## Purpose

P10-C lets **material decisions be evaluated against deterministic
simulation/optimization before authorization**. It composes the existing S363
governed simulation path with a bounded evaluation gate the governance layer
consults before an `ExecutionCommand` is authorized.

```text
AgentProposal (P10-B)
        ↓
SimulationStep(s) -> S363 governed simulation (dry-run only, no side effect)
        ↓
AgentSimulationEvaluation (deterministic, content-addressed)
        ↓
evaluation gate consulted before authorization
```

## Contract

`src/scm_ontology/simulation_before_execution.py`:

- **`AgentSimulationEvaluation`** — an immutable, content-addressed evaluation
  bundling the `GovernedSimulationResult`, a `feasible` verdict, and the
  rationale the authorization layer consults.
- **`evaluate_simulation_before_execution(...)`** — runs the deterministic
  simulation (S363 dry-run path) and produces the bounded evaluation.

### Boundaries

| what | allowed |
|---|---|
| simulations | deterministic, dry-run only, no external side effect |
| evaluation output | `feasible` / `infeasible` guidance + run trace |
| authorization decision | remains governed (P10-C only informs, never authorizes) |

## Fail-closed behavior

- `context_id` must be non-empty.
- At least one `SimulationStep` is required.
- An infeasible simulation yields `feasible = False` guidance that blocks
  authorization rather than silently proceeding.

## Guardrails

- P10-C performs no external side effect and introduces no new canonical
  semantics.
- Simulation informs, but never overrides, the governed authorization boundary.
