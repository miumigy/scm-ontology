# S141 — Measure

S141 defines the SCM OS Measure semantic for observing execution and resulting world state, creating measurements, evaluating metrics and KPIs, and preserving the distinction between measurement, evaluation, and decision.

## Measure contract

```text
Execution / State / Event
          ↓
      Observation
          ↓
      Measurement
          ↓
   Metric / KPI Value
          ↓
 Performance Assessment
          ↓
 Decision / Learning
```

Measurement records what was observed or measured. It does not itself explain causality, declare performance, or make a decision.

## Core boundaries

- Observation ≠ Measurement
- Measurement ≠ Metric
- Metric ≠ KPI
- KPI ≠ Target
- Target ≠ Actual
- Measurement ≠ Performance Assessment
- Performance ≠ Diagnosis
- Performance Assessment ≠ Decision
- Actual ≠ Inferred

S112 remains the canonical semantic foundation for these concepts; S141 connects them to the SCM OS closed loop rather than redefining them.

## Execution-to-measurement

Execution may produce events, state changes, and evidence. These become observations or measurement inputs without implying that execution was successful or that the resulting performance is satisfactory.

```text
Action → Execution → State Change / Event → Observation → Measurement
```

## Actual and epistemic status

Measured actuals must retain source, method, unit, observation time, transaction time, uncertainty, and provenance where available. Missing or stale data must not silently become zero or current.

Estimated, predicted, and inferred values remain epistemically distinct from measured actuals.

## Metric and KPI evaluation

A Metric Value is interpreted according to its Metric Definition, scope, period, granularity, aggregation, and version. A KPI adds governance semantics such as owner, target, threshold, status, or score.

A KPI status is a derived assessment and must not be mistaken for the underlying measurement.

## Performance and variance

Performance assessment may compare actual measurements against targets, baselines, benchmarks, commitments, plans, or scenarios. Variance and deviation are derived concepts and preserve their reference basis.

```text
Actual Measurement
       ↓ compare with
Target / Baseline / Plan / Commitment
       ↓
Variance / Deviation / Adherence / Accuracy
       ↓
Performance Assessment
```

The comparison basis must remain explicit; a number called `variance` without its reference is semantically incomplete.

## Provenance and reproducibility

Measurement and metric values should retain provenance and lineage sufficient to explain how the value was obtained. Restatements and revisions must not erase historical values without an explicit lineage relationship.

## Scenario and counterfactual measurement

Scenario and counterfactual performance remain scoped to their world. They may be compared with actual performance but cannot silently become actual observations.

## Closed-loop connection

```text
Observe
  ↓
Diagnose
  ↓
Plan
  ↓
Decide
  ↓
Execute
  ↓
Measure
  ↓
Learn
  ↺
```

Measure feeds both Diagnose and Learn. It may trigger a new diagnosis when a deviation or exception is detected, but measurement itself is not diagnosis.

## Non-goals

S141 does not define a BI dashboard, KPI visualization, data warehouse schema, statistical engine, or specific measurement protocol. It defines canonical semantics for connecting observed execution and state to reproducible performance evidence.
