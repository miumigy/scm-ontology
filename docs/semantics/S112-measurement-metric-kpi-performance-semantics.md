# S112 — Measurement, Metric, KPI & Performance Semantics

S112 defines the semantics required to observe, measure, compare, evaluate, and govern Supply Chain performance without confusing observations, measurements, metrics, targets, KPIs, and decisions.

## Core principle

```text
Observation
   ↓ measurement
Measurement
   ↓ definition / computation
Metric
   ↓ selection / governance
KPI
   ↓ evaluation against target / threshold
Performance Assessment
   ↓
Decision
```

These concepts are related but are not interchangeable.

## Observation

An Observation is an assertion about something observed at a reference time, place, or context.

Examples:

```text
truck arrived at 10:42
inventory count was 720
shipment temperature was 4.2°C
```

Observation may originate from a sensor, person, system, transaction, or external source.

## Measurement

A Measurement is an observation expressed through a defined measurable quantity, unit, scale, or measurement method.

```text
inventory = 720 units
arrival delay = 42 minutes
temperature = 4.2 °C
```

Measurement semantics must preserve unit and reference context where applicable.

## Measurement versus Observation

An Observation may be qualitative or unstructured.

A Measurement has an explicit measurable interpretation.

```text
Observation: "truck was late"
Measurement: 42 minutes late
```

## Measurement source

A Measurement should preserve its source where material.

Examples:

```text
sensor
manual count
ERP transaction
WMS event
TMS event
external provider
inference model
```

This connects to S104 Provenance and S103 Epistemic Semantics.

## Measurement method

A Measurement may depend on a defined method.

Examples:

```text
physical count
cycle count
GPS timestamp
system transaction timestamp
statistical estimation
model inference
```

Different methods may produce different measurements for the same underlying phenomenon.

## Measurement uncertainty

Measurements may have uncertainty, tolerance, precision, or confidence.

```text
inventory = 500 ± 20
confidence = 0.92
```

Uncertainty must not be silently discarded when material to a decision.

## Unit of measure

A Measurement may require a Unit of Measure.

Examples:

```text
kg
cases
units
pallets
hours
JPY
CO2e
minutes
percent
```

Conversions must preserve dimensional meaning.

## Measurement scale

A measurement may use a scale such as:

```text
ratio
interval
ordinal
nominal
binary
```

The scale constrains valid mathematical operations.

## Measurement timestamp

A Measurement may have multiple relevant times:

```text
observed_at
measured_at
recorded_at
reported_at
received_at
```

These must not be collapsed when temporal distinctions matter.

## Metric

A Metric is a defined quantitative or qualitative measure derived from one or more Measurements, Events, States, or other data.

Examples:

```text
fill rate
inventory turnover
OTIF
lead time
forecast accuracy
capacity utilization
```

A Metric is a semantic definition, not merely a number.

## Metric definition

A Metric Definition specifies how a Metric is constructed.

It may define:

```text
name
meaning
formula
inputs
units
granularity
population
time window
aggregation
filters
inclusion / exclusion rules
version
```

## Metric value

A Metric Value is an evaluated instance of a Metric Definition for a specified context and period.

```text
Metric: Fill Rate
Period: 2026-08
Value: 94.2%
```

Metric Definition and Metric Value are distinct entities.

## Metric identity

Two values with the same display name are not necessarily the same Metric.

Identity should consider semantic definition and applicable version.

```text
"OTIF"
  ≠ automatically
same metric across organizations
```

## Metric version

Metric definitions may change.

```text
OTIF v1
   ↓
OTIF v2
```

Historical Metric Values should retain the definition/version under which they were calculated.

## Metric granularity

A Metric may be evaluated at different granularities.

Examples:

```text
shipment
order line
customer
product
lane
facility
region
enterprise
```

Aggregation across granularities is not automatically valid.

## Metric scope

Metric Scope defines the population and boundary over which a Metric applies.

```text
all shipments
Japan domestic shipments
customer X
product family Y
```

Scope must be explicit for meaningful comparison.

## Metric period

A Metric may refer to a defined time window.

Examples:

```text
day
week
month
quarter
rolling 90 days
order lifecycle
```

The period semantics must be explicit.

## Metric aggregation

Metric aggregation describes how observations or lower-level values are combined.

Examples:

```text
sum
count
mean
median
weighted mean
minimum
maximum
percentile
ratio
```

Aggregation is part of Metric semantics.

## Ratio metric

A Ratio Metric is calculated from a numerator and denominator.

```text
fill rate = fulfilled quantity / requested quantity
```

The numerator and denominator populations must be defined explicitly.

## Rate metric

A Rate expresses occurrence or quantity relative to a defined basis and period.

```text
orders/hour
late shipments/day
units/customer/month
```

Rate and ratio should not be treated as synonymous without definition.

## Stock metric

A Stock Metric describes a quantity at a point or state.

Examples:

```text
on-hand inventory
backlog
available capacity
cash balance
```

Stock metrics differ from flow metrics.

## Flow metric

A Flow Metric measures quantity accumulated over a period.

Examples:

```text
shipments/week
production/month
sales/year
```

Confusing stock and flow metrics can create materially incorrect analysis.

## Duration metric

A Duration Metric measures elapsed time between defined temporal events or states.

Examples:

```text
lead time
cycle time
waiting time
dwell time
```

The start and end events must be explicit.

## Performance

Performance is an assessment of how an observed or measured result relates to a defined objective, target, expectation, constraint, or benchmark.

Performance is therefore contextual.

```text
Actual
  ↓ compare
Target / Expectation
  ↓
Performance Assessment
```

## Target

A Target is a desired or governed value or range for a Metric under a defined context.

```text
OTIF target = 95%
```

Target is not the same as actual performance.

## Threshold

A Threshold defines a boundary at which a condition, alert, status, or decision rule may change.

```text
inventory < safety threshold
```

Threshold semantics connect to S107 Constraint / Policy / Rule semantics.

## Tolerance

A Tolerance defines an acceptable deviation around a target, requirement, or reference.

```text
due time = 10:00
acceptable tolerance = ±15 min
```

Tolerance is not necessarily a target.

## Benchmark

A Benchmark is a reference value used for comparison.

Examples:

```text
industry benchmark
historical best
peer group
internal standard
```

Benchmark does not automatically imply a required target.

## Baseline

A Baseline is a defined reference state against which change or improvement is evaluated.

```text
baseline cost = 100
current cost = 92
improvement = 8%
```

Baseline semantics must preserve the reference period and definition.

## KPI

A Key Performance Indicator (KPI) is a Metric explicitly selected and governed as important for evaluating a defined objective, responsibility, or decision context.

Not every Metric is a KPI.

```text
Metric
  ↓ governance / selection
KPI
```

## KPI context

A KPI should identify its relevant:

```text
objective
owner / accountable Actor
scope
period
target
threshold
review cadence
governance rule
```

## KPI target

A KPI may have one or more targets by context.

```text
OTIF
 ├─ customer segment A: 98%
 ├─ customer segment B: 95%
 └─ internal transfer: 92%
```

Targets are contextual rather than necessarily universal.

## KPI status

A KPI Status is a derived classification based on Metric Value and applicable Target / Threshold / Rule.

Examples:

```text
on_target
warning
breach
unknown
not_applicable
```

Status must be derived from explicit rules.

## KPI ownership

Ownership should distinguish:

```text
metric owner
KPI owner
accountable Actor
measurement source
decision authority
```

These roles are not automatically identical.

## KPI versus Decision

A KPI describes or assesses performance.

A Decision determines an action or policy response.

```text
KPI: OTIF = 89%
       ↓
Decision: change carrier allocation
```

The KPI does not itself constitute the Decision.

## KPI versus Objective

An Objective expresses a desired outcome.

A KPI measures or assesses progress toward an Objective.

```text
Objective: improve customer service
KPI: OTIF
```

One Objective may have multiple KPIs.

## KPI versus Target

```text
KPI
  = what is measured / governed

Target
  = desired value
```

They must remain separate.

## Actual versus Target

An Actual Metric Value represents what occurred or was measured.

A Target represents what is desired or required.

```text
actual = 91%
target = 95%
```

The difference is an evaluation, not a replacement of either value.

## Variance

Variance represents a defined difference between two comparable values.

Examples:

```text
actual - plan
actual - target
forecast - actual
budget - actual
```

The comparison basis must be explicit.

## Deviation

Deviation represents difference from a reference state, path, plan, schedule, or requirement.

Examples:

```text
planned route vs actual route
scheduled time vs actual time
planned quantity vs actual quantity
```

Variance and Deviation are related but not universally interchangeable.

## Adherence

Adherence evaluates whether actual behavior remained within the defined requirements of a Plan, Schedule, Policy, or Commitment.

```text
Schedule Adherence
Plan Adherence
Commitment Adherence
```

Adherence semantics require the reference definition.

## Accuracy

Accuracy evaluates the closeness of a prediction or estimate to an observed or actual result.

Examples:

```text
forecast accuracy
ETA accuracy
inventory estimate accuracy
```

Accuracy should not be conflated with bias or precision.

## Bias

Bias describes systematic directional difference between predictions or estimates and actual observations.

```text
forecast consistently +10%
```

Bias is distinct from random error.

## Precision

Precision describes consistency or granularity of repeated measurements or estimates.

A measurement can be precise but inaccurate.

## Forecast accuracy

Forecast Accuracy is a derived Metric comparing Forecast and Actual Demand under a defined method, population, horizon, and aggregation.

Different formulas may produce different results.

The formula must therefore be part of Metric Definition.

## Forecast error

Forecast Error measures the difference between Forecast and Actual Demand under a specified convention.

Examples:

```text
actual - forecast
forecast - actual
absolute error
percentage error
```

Sign convention must be explicit.

## Service performance

Service Performance evaluates fulfillment against service requirements or targets.

Examples:

```text
OTIF
fill rate
perfect order
response time
availability
```

S109 defines the underlying fulfillment semantics.

## Cost performance

Cost Performance evaluates actual or expected Cost relative to a defined reference.

Examples:

```text
actual vs budget
actual vs standard cost
freight cost per unit
cost-to-serve
```

Cost itself is not defined by S112; S112 defines its measurement semantics.

## Capacity performance

Capacity Performance evaluates use, availability, utilization, efficiency, or constraint violations relative to defined capacity semantics.

Examples:

```text
capacity utilization
throughput per hour
capacity attainment
```

## Inventory performance

Inventory Performance evaluates Inventory State and Flow against defined objectives.

Examples:

```text
inventory turns
days of supply
stockout rate
excess inventory
inventory accuracy
```

## Flow performance

Flow Performance evaluates movement through the Supply Chain Network.

Examples:

```text
transit time
on-time departure
on-time arrival
lane utilization
route adherence
```

## Composite KPI

A Composite KPI combines multiple Metrics according to an explicit formula or decision rule.

```text
Perfect Order
 = on-time
 + complete
 + damage-free
 + documentation-compliant
```

The component definitions must remain separately inspectable.

## Weighted KPI

A Weighted KPI combines component Metrics using explicit weights.

```text
score = 0.4 × service + 0.3 × cost + 0.3 × inventory
```

Weights are semantic parameters and should be versioned.

## KPI score

A KPI Score is a derived representation of performance according to a defined scoring function.

A score should not be mistaken for the underlying measurement.

## Alert

An Alert is a generated notification or signal triggered by a defined condition.

```text
KPI status = breach
      ↓
Alert
```

Alert generation is a Decision / Rule application, not a Metric itself.

## Exception

An Exception represents a condition requiring attention because it deviates from an expected, permitted, or governed state.

Exception semantics connect to S107 and operational semantics from S108/S109.

## Performance assessment

A Performance Assessment is a contextual judgment derived from Metrics and comparison references.

It may include:

```text
result
status
severity
confidence
explanation
reference
```

It is not necessarily an objective fact.

## Performance attribution

Performance Attribution identifies contributing Actors, Nodes, Lanes, Products, Processes, Resources, or Events associated with a Performance result.

Attribution should distinguish:

```text
correlation
causal contribution
responsibility
```

S101 governs causal semantics.

## Performance decomposition

A high-level KPI may be decomposed into lower-level contributing Metrics.

```text
Service KPI
 ├─ On-time
 ├─ Complete
 ├─ Quality
 └─ Documentation
```

Decomposition is not automatically causal decomposition.

## Performance aggregation

Aggregating performance across entities requires an explicit aggregation method.

For example, enterprise OTIF should not automatically be the arithmetic mean of facility OTIF values when shipment volumes differ.

Weighted aggregation may be required.

## Denominator integrity

Ratio Metrics require denominator integrity.

A denominator should specify:

```text
population
filters
period
unit
exclusions
```

Otherwise two apparently identical percentages may represent different populations.

## Missing data

Missing Measurements must remain distinguishable from zero.

```text
missing ≠ 0
```

Missingness may affect Metric validity.

## Unknown KPI status

If required inputs are unavailable or invalid, KPI Status may be `unknown` rather than forcing a numeric or binary result.

## Stale data

A Measurement or Metric Value may be stale relative to the decision context.

Freshness is temporal metadata, not an automatic quality judgment.

## Metric comparability

Two Metric Values are comparable only when their semantic definitions, units, scopes, periods, and relevant calculation rules are compatible.

```text
same name
  ≠
same metric
```

## Cross-system metric mapping

Different enterprise systems may expose different definitions for the same business term.

```text
ERP OTIF
TMS OTIF
BI OTIF
```

SCM Ontology should map them to a canonical Metric Definition while retaining source semantics and provenance.

## Metric lineage

A Metric Value should be traceable to its source Measurements, Events, States, or transactions where material.

```text
Metric Value
   ↓ lineage
Measurements / Events
   ↓
Source records
```

This enables auditability and root-cause analysis.

## Metric reproducibility

A Metric Value should be reproducible where practical from:

```text
Metric Definition version
source data
filters
period
aggregation
parameters
```

This is essential for governed analytics.

## Metric snapshot

A Metric Snapshot represents the calculated state of one or more Metrics at a reference time.

It may support dashboards and reporting while retaining underlying definitions.

## Performance period close

A reporting period may be closed or restated.

Restatement should preserve the prior reported value and identify the reason for revision where governance requires it.

## Restatement

A Metric Value may be recalculated because source data, definitions, or rules changed.

```text
reported value v1
       ↓ restatement
reported value v2
```

Historical values should not be silently overwritten when auditability matters.

## Target revision

Targets may change over time.

```text
Target v1
   ↓
Target v2
```

A historical Performance Assessment should use the Target applicable at the relevant evaluation context unless explicitly performing a retrospective comparison.

## Performance scenario

Performance may be evaluated under scenarios.

```text
Actual performance
Scenario A
Scenario B
```

Scenario values must remain distinguishable from actual values.

## Counterfactual performance

A Counterfactual Performance Value represents what performance might have been under an alternative Decision, Route, Policy, or Network State.

S102 governs counterfactual semantics.

## Performance uncertainty

A Performance Assessment may include uncertainty or confidence.

```text
OTIF = 94.2%
confidence = 0.88
```

This is particularly important for inferred or incomplete measurements.

## Metric-driven decision

A Metric or KPI may provide evidence for a Decision but does not automatically determine it.

```text
Observation
 ↓
Measurement
 ↓
Metric
 ↓
KPI
 ↓
Evaluation
 ↓
Decision
```

The Decision remains governed by S107.

## KPI feedback loop

S112 connects performance to closed-loop SCM:

```text
Execution
   ↓
Observation
   ↓
Measurement
   ↓
Metric
   ↓
KPI
   ↓
Performance Assessment
   ↓
Decision
   ↓
Plan / Schedule
   ↓
Execution
```

This provides the measurement layer required for a continuously learning SCM system.

## Non-goals

S112 does not define a universal KPI catalog, dashboard layout, BI tool schema, accounting standard, statistical methodology, forecasting algorithm, or enterprise reporting architecture.
