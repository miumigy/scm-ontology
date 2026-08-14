# S121 — Planning / S&OP / PSI Semantic Mapping

## Purpose

S121 applies the S119 mapping contract to planning semantics used by demand planning, supply planning, S&OP, and PSI management.

The objective is to preserve planning intent, time horizon, version, scenario, and actual outcome without collapsing them into a single forecast or plan object.

## Canonical mapping boundary

```text
Planning Source
  ├─ Forecast
  ├─ Demand Plan
  ├─ Supply Plan
  ├─ Production Plan
  ├─ Inventory Plan
  └─ S&OP Decision
        ↓
Semantic Mapping
        ↓
Canonical Demand / Supply / Inventory / Plan / Decision
```

## Forecast is not Demand

A forecast is an epistemic assertion about expected future demand. Demand is the canonical business phenomenon/request represented by the model.

```text
Forecast ≠ Demand
Forecast ≠ Actual
Forecast ≠ Order
```

Forecast values should retain their origin, issue time, validity period, horizon, version, and epistemic status.

## Plan is not Forecast

```text
Forecast → expectation
Plan     → intended course of action
```

A supply plan can respond to a forecast but is not itself a prediction.

## PSI semantics

PSI is treated as a planning/view pattern, not a new Core Ontology entity.

```text
Production Plan → Supply / Transformation / Plan
Sales or Demand Plan → Demand / Plan
Inventory Plan → Inventory / Plan
```

The PSI view may relate these concepts across a common time bucket, but must not redefine them.

## S&OP semantics

S&OP is a decision and governance process, not a canonical physical object.

The mapping should preserve:

```text
Demand / Supply evidence
        ↓
Evaluation / Scenario
        ↓
Recommendation
        ↓
Decision
        ↓
Plan / Commitment / Action
```

Recommendation must not be silently mapped as Decision.

## Time and version semantics

Planning records commonly contain:

- issue time
- effective/planning period
- horizon
- bucket
- version
- scenario
- planned quantity
- actual quantity

These must remain distinct. A later plan version does not rewrite an earlier historical plan.

## Scenario integration

Scenario and counterfactual semantics remain governed by S102.

```text
Baseline Plan
Alternative Scenario
Counterfactual Plan
Actual Outcome
```

A scenario result must not be stored as actual execution merely because it was selected for comparison.

## Actual reconciliation

Planning mappings should support reconciliation without overwriting history.

```text
Plan v1 ─┐
Plan v2 ─┼→ Variance / Performance
Actual ──┘
```

The actual remains an observation/measurement of what occurred, while the plan remains what was intended at its issue/version context.

## Metric boundary

PSI and S&OP implementations often contain KPIs such as forecast accuracy, service level, inventory turns, and plan adherence. These remain S112 Measurement/Metric/KPI concepts rather than becoming planning entities.

## Non-goals

S121 does not define a universal S&OP process, planning algorithm, forecasting method, MRP logic, or vendor-specific APS schema.

## Exit criteria

A planning source can map forecast, demand plan, supply plan, inventory plan, and S&OP decision data to canonical semantics while preserving epistemic, temporal, scenario, version, provenance, and planned/actual distinctions.
