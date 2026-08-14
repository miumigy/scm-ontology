# S132 — What-if Reasoning

S132 defines the semantic contract for evaluating an alternative decision or intervention against an explicit scenario without rewriting actual history.

## Reasoning contract

```text
Actual State
   ↓ baseline
Alternative Decision / Intervention
   ↓ scenario
Counterfactual Scenario
   ↓ constraints + causal model
Hypothetical Outcome
   ↓ assessment
What-if Result
```

A what-if result is hypothetical. It is not an Actual Outcome, Forecast, or Decision.

## Required boundaries

- What-if ≠ Forecast
- Counterfactual ≠ Actual History
- Alternative Decision ≠ Actual Decision
- Hypothetical Outcome ≠ Actual Outcome
- Scenario Evaluation ≠ Execution
- Recommendation ≠ Decision

## Baseline

A scenario should identify the baseline state or world from which the alternative is evaluated. Baseline references must remain immutable from the perspective of the scenario result.

## Intervention

An intervention represents an alternative decision, policy, network state, capacity assumption, demand assumption, or other explicit change. The intervention must be distinguishable from an executed Action.

```text
Alternative Decision
      ≠
Executed Action
```

## Constraints

What-if reasoning may evaluate constraints inherited from the baseline or explicitly changed for the scenario. Constraint evaluation uses S130 semantics; `unknown` is never silently treated as `satisfied`.

## Causal connection

Causal reasoning from S131 may be used to assess effects of an intervention. A causal assessment remains an assessment and does not turn the scenario into historical fact.

## Epistemic status

Scenario outcomes should preserve their epistemic status, for example:

- simulated
- estimated
- inferred
- unknown

A simulated outcome must not be represented as an observed or actual outcome.

## Provenance and reproducibility

A what-if result should retain references to:

- baseline state
- intervention
- scenario
- constraints
- evidence/model inputs
- reasoning method where available

This enables reproducibility and explanation without requiring a particular simulation or optimization engine.

## Temporal scope

The scenario has its own temporal context. Planned, promised, actual, and scenario times remain distinct under S124.

## Non-goals

S132 does not prescribe an optimization solver, simulation engine, probabilistic model, or decision policy. It defines the semantics required for those implementations to produce safely scoped what-if results.
