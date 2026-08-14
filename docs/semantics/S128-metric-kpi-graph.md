# S128 — Metric / KPI Graph

## Purpose

Project S112 Measurement / Metric / KPI semantics into the SCM Graph while preserving the distinction between observation, measurement, metric, KPI, target, and decision.

## Canonical chain

```text
Observation
    ↓ measured_as
Measurement
    ↓ aggregated_as / derived_as
Metric Value
    ↓ evaluates
KPI
    ↓ assessed_as
Performance Assessment
    ↓ informs
Recommendation / Decision
```

This is a semantic projection, not a requirement for a particular graph database.

## Core boundaries

```text
Observation ≠ Measurement
Measurement ≠ Metric
Metric ≠ KPI
KPI ≠ Target
Target ≠ Actual
Performance Assessment ≠ Decision
Recommendation ≠ Decision
```

A metric value is a value within a metric definition and scope. A KPI adds governance meaning such as owner, status, or target context. A target does not become an actual merely because a KPI evaluates it.

## Metric lineage

A metric value should remain traceable to its contributing measurements and, where available, observations.

```text
Observation
    ↓
Measurement
    ↓
Metric Value
    ↓
KPI Score / Status
    ↓
Performance Assessment
```

Aggregation or derivation must not erase source period, scope, granularity, unit, or provenance semantics.

## Target and actual

Target, threshold, tolerance, benchmark, baseline, and actual value are separate graph concepts or references. Variance/deviation may relate them but must not replace either value.

## Reproducibility and restatement

Metric definitions and versions remain explicit. Restated metric values should retain lineage to the prior assertion where applicable rather than silently overwriting historical results.

## Scenario and counterfactual performance

A metric or KPI evaluated in a scenario remains scenario-scoped.

```text
Actual Performance
    ≠
Scenario Performance
    ≠
Counterfactual Performance
```

Scenario performance may be compared with actual performance, but must not overwrite it.

## Decision connection

The graph may represent:

```text
Performance Assessment
        ↓ informs
Recommendation
        ↓ considered_by
Decision
        ↓ results_in
Action
```

The graph must not infer that every KPI breach caused a decision. Causal semantics remain governed by S126.

## Example traversal questions

The projection should support questions such as:

- What observations contributed to this KPI score?
- Which metric definition and version produced this value?
- Which target and tolerance were in effect?
- Which performance assessment followed the KPI evaluation?
- Which decision considered that assessment?
- Which source evidence supports the underlying measurements?
- Is this value actual, planned, estimated, or scenario-specific?

## Design boundary

S128 defines graph semantics for metrics and KPIs. It does not define a universal KPI catalog, business-specific thresholds, optimization logic, or causal inference.
