# S127 — Scenario / Counterfactual Graph

## Purpose

S127 projects the S102 Scenario / Counterfactual semantics into the SCM Graph without allowing hypothetical worlds to overwrite actual history.

## World separation

```text
Actual World
   ├── Scenario A
   ├── Scenario B
   └── Counterfactual C
```

An `Actual` graph represents observed or asserted history. A `Scenario` represents an alternative world/model state. A `Counterfactual` represents a hypothetical alternative conditioned on a stated change.

## Core boundaries

```text
Scenario ≠ Actual History
Counterfactual ≠ Forecast
Counterfactual ≠ Actual
Alternative Decision ≠ Actual Decision
Alternative Network State ≠ Actual Network State
```

A forecast can exist inside a scenario, but a forecast is not itself a counterfactual.

## Projection

A scenario graph is a graph context that may contain copies/references of canonical entities and relationships with scenario-specific state.

```text
Canonical Entity
      ↓ referenced_by
Scenario Entity State
      ↓ affected_by
Alternative Decision
      ↓ results_in
Scenario Outcome
```

The scenario graph should preserve references to the actual-world entities from which the scenario was constructed.

## Counterfactual semantics

A counterfactual should identify:

- reference world
- intervention or changed condition
- affected entities/relationships
- resulting hypothetical state or outcome
- uncertainty
- provenance of the counterfactual construction

Example:

```text
Actual:
  Factory capacity = 100
  Demand = 90
  Service level = 98%

Counterfactual:
  intervention: capacity = 80
  → hypothetical service level = 91%
```

The hypothetical service level must not replace the actual 98% observation.

## Scenario lineage

Scenario construction retains lineage:

```text
Actual State
   ↓ scenario_basis
Scenario
   ↓ intervention
Alternative State
   ↓ simulation / reasoning
Scenario Outcome
```

This connects S102 to S104 Provenance, S106 Temporal, S125 Provenance Graph, and S126 Causal Graph.

## Decision comparison

Alternative decisions can be represented without claiming that they were executed.

```text
Actual Decision
Alternative Decision A
Alternative Decision B
        ↓
Scenario Outcomes
```

Only an execution event in the actual world establishes actual execution.

## Graph safety rules

1. Scenario nodes must carry an explicit scenario/world context.
2. Counterfactual edges must identify their reference world.
3. Scenario outcomes must not be written into actual state.
4. Planned, predicted, inferred, and counterfactual values retain their epistemic status.
5. Scenario-derived metrics retain lineage to their scenario and source assumptions.
6. A scenario may reference actual entities without becoming actual history.

## Non-goals

S127 does not implement simulation, optimization, forecasting, or causal inference. It defines graph representation semantics for those future engines.
