# S102 — Scenario, Counterfactual & What-if Semantics

S102 defines the semantic boundary between historical reality, scenario, projection, forecast, plan, simulation, counterfactual, and what-if analysis.

## Canonical decision

Historical Reality and hypothetical alternatives must remain distinguishable.

```text
Historical Reality
      │
      ├── Actual Path
      │
      └── Hypothetical / Scenario Paths
```

A Scenario is a modeled or assumed state/path used to explore possible consequences. It is not itself a historical Observation.

## Actual / Historical Reality

Historical Reality represents what is asserted to have actually occurred in the modeled domain.

```text
Actual Observation
Actual Action
Actual Outcome
```

These may be supported by provenance and evidence according to the existing Observation and Evidence semantics.

Historical Reality should not be overwritten by a later scenario result.

## Scenario

A Scenario is a coherent set of assumptions, conditions, decisions, or parameter values under which alternative consequences can be explored.

Examples:

```text
Demand +20%
Supplier lead time +5 days
Plant capacity -10%
Port A unavailable
```

A Scenario is a modeling context, not a claim that the conditions actually occurred.

## Scenario versus Plan

A Plan expresses intended future action or commitment.

A Scenario expresses an assumed or hypothetical context.

```text
Scenario:
  Supplier B unavailable

Plan:
  Use Supplier C
```

A Plan may be evaluated under a Scenario, and a Scenario may contain alternative plans, but they are not synonyms.

## Scenario versus Forecast

A Forecast is an estimate or prediction about a future or unknown value based on a defined method and information set.

A Scenario is a conditional context.

```text
Forecast:
  expected demand = 1,050

Scenario:
  demand = 1,200
```

A scenario may use a forecast as an input, and a forecast may be produced separately for multiple scenarios.

## Scenario versus Projection

A Projection is a modeled continuation or estimate of a trajectory under specified assumptions.

A Scenario is the assumption/context set under which one or more projections may be generated.

```text
Scenario assumptions
       ↓
Projection
```

The distinction should be preserved where scenario provenance matters.

## Simulation

A Simulation is a computational or analytical process that generates modeled behavior under specified inputs, rules, and assumptions.

```text
Scenario
   ↓
Simulation
   ↓
Projected / simulated outcomes
```

A simulation result is not automatically a historical Observation.

## Counterfactual

A Counterfactual represents a hypothetical alternative to an actual historical or realized path, typically asking what would have happened if a specified condition or Action had been different.

```text
Actual:
  Action A → Outcome O

Counterfactual:
  no Action A → hypothetical Outcome O'
```

The counterfactual path is not asserted as historical reality.

## Counterfactual versus Scenario

A Scenario may be prospective, exploratory, or hypothetical without reference to an actual realized path.

A Counterfactual is specifically related to an alternative to a known or asserted actual path.

```text
Scenario:
  What if demand is +20% next month?

Counterfactual:
  What if last month's replenishment had not been expedited?
```

## What-if

What-if is an analytical question or operation that evaluates consequences under changed assumptions, decisions, or conditions.

It is therefore better understood as an analysis relationship/process than as a universal data object.

```text
What-if question
      ↓
Scenario / Counterfactual
      ↓
Model / Simulation / Analysis
      ↓
Result
```

## Scenario assumptions

A Scenario should make its assumptions identifiable when reproducibility matters.

Conceptually:

```text
Scenario
├─ reference context
├─ assumptions
├─ changed variables
├─ constraints
├─ candidate decisions
├─ model / method
└─ horizon
```

S102 does not require all fields in every implementation.

## Scenario versioning

Scenario definitions may evolve.

```text
Scenario v1
Scenario v2
Scenario v3
```

A result should be attributable to the scenario definition and relevant model/version when reproducibility matters.

Changing a Scenario must not rewrite historical Observations.

## Scenario branch

A scenario may be understood as a branch from a common reference context.

```text
                    Base Context
                        │
             ┌──────────┴──────────┐
             ↓                     ↓
        Scenario A            Scenario B
             ↓                     ↓
        Result A               Result B
```

The branch represents modeling divergence, not historical divergence.

## Scenario comparison

Results from different scenarios may be compared under a common evaluation framework.

```text
Scenario A → Result A
Scenario B → Result B
        ↓
Comparison
        ↓
Decision support
```

Scenario comparison does not imply that either scenario is historical reality.

## Counterfactual comparison

A counterfactual analysis compares an actual outcome with a hypothetical alternative.

```text
Actual Outcome O
       │
       ├──── compare ──── Counterfactual Outcome O'
       │
       ↓
Estimated effect / difference
```

The estimated difference is not itself proof that the hypothetical path would have occurred.

## Counterfactual uncertainty

Counterfactual results generally carry uncertainty because the alternative path is not directly observed.

```text
Historical Observation
  = observed evidence

Counterfactual Result
  = modeled / inferred alternative
```

The ontology must not represent them as equivalent epistemic artifacts.

## Model dependence

Scenario and counterfactual results depend on the model, assumptions, parameters, and data used to generate them.

Therefore:

```text
same Scenario
   + different Model
   → potentially different Result
```

Model identity/version should be retained where reproducibility matters.

## Scenario result versus Outcome

A modeled scenario result predicts or estimates what could happen under the scenario.

An Actual Outcome describes what resulted from an actual Decision or Action.

```text
Scenario Result
  ≠
Actual Outcome
```

A scenario result may later be compared with an actual Outcome after the scenario's horizon has materialized.

## Scenario result versus Observation

A simulated or projected value is not automatically an Observation.

For example:

```text
Simulation:
  projected inventory = 480

Actual Observation:
  inventory = 512
```

The values may be compared, but their provenance and epistemic status remain distinct.

## Scenario materialization

A Scenario may become relevant to actual operations when its assumptions materialize in reality.

This does not transform the Scenario itself into historical reality.

Instead:

```text
Scenario assumption
       ↓
Actual condition occurs
       ↓
Observation of actual condition
```

The actual Observation is a new historical artifact.

## Decision under Scenario

A Decision may be evaluated under a Scenario before execution.

```text
Scenario
   ↓
Candidate Decision
   ↓
Simulation / Evaluation
   ↓
Expected Result
```

The Decision remains hypothetical until adopted under the applicable decision authority semantics.

## What-if optimization

An optimization system may generate candidate decisions under multiple scenarios.

```text
Scenario A
  ├─ Decision A1
  └─ Decision A2

Scenario B
  ├─ Decision B1
  └─ Decision B2
```

Optimization output is a recommendation or analytical result until a Decision is actually authorized under S100.

## Relationship to Forecast

A forecast can be an input to a Scenario.

```text
Forecast
   ↓
Scenario assumptions
   ↓
Simulation / Projection
```

Alternatively, a forecasting method may generate separate forecasts conditional on different Scenarios.

The ontology should preserve the direction of dependency rather than treating forecast and scenario as synonyms.

## Relationship to Plan

A Plan may be evaluated across scenarios.

```text
Plan P
 ├─ Scenario A → Result A
 ├─ Scenario B → Result B
 └─ Scenario C → Result C
```

This supports robust planning without conflating planning intent with scenario assumptions.

## Relationship to Actual Closed Loop

S100 and S101 define the actual operational loop:

```text
Observation
 → Evaluation
 → Decision
 → Action
 → Outcome
 → Observation
```

S102 adds an analytical branch:

```text
Observation / Context
        ↓
Scenario / Counterfactual
        ↓
Simulation / Projection
        ↓
Expected Result
        ↓
Decision Support
```

The analytical branch must not be mistaken for an actual execution path.

## Reality boundary

The ontology should be able to answer:

```text
Did this actually happen?
Was it observed?
Was it planned?
Was it forecast?
Was it simulated?
Was it hypothetical?
Was it counterfactual?
```

This reality-status distinction is fundamental for trustworthy AI and SCM decision support.

## No mandatory scenario fields on Observation

S102 does not add fields such as:

```text
scenario_id
forecast
simulation_result
counterfactual
what_if
projection
```

to the canonical Observation primitive.

These belong to Scenario, Forecast, Simulation, Projection, Counterfactual, or analytical result models.

## Non-goals

S102 does not define a universal forecasting algorithm, simulation engine, optimization method, scenario-planning framework, digital-twin architecture, probability model, or counterfactual inference algorithm.
