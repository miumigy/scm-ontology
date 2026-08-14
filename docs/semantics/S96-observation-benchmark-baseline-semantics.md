# S96 — Observation Benchmark & Baseline Semantics

S96 defines the semantic roles of references used to contextualize Observation comparisons, including baseline, benchmark, target, reference, and plan/forecast versions.

## Canonical decision

A comparison reference is contextual metadata for a comparison, not an intrinsic property of the Observation being evaluated.

```text
Observed Observation
        │
        │ compared against
        ▼
Reference Observation / Reference Result
        │
        ▼
Comparison Context
        │
        ▼
Difference / Variance / Ratio
```

The canonical Observation primitive remains unchanged.

## Baseline

A baseline is a declared reference state or value against which change or performance is evaluated.

```text
baseline = approved reference at a defined point/context
```

A baseline must have an explicit scope, temporal context, and semantic definition appropriate to the comparison.

A baseline is not synonymous with the latest value or the prior value.

## Benchmark

A benchmark is a reference used to assess performance or position relative to a defined comparator.

Examples:

```text
industry benchmark
peer benchmark
best-practice benchmark
historical benchmark
internal benchmark
```

A benchmark may be an Observation, an aggregate result, a target-derived reference, or another domain result depending on the contract.

## Target

A target expresses an intended or desired value/condition.

```text
Actual = observed/result value
Target = intended reference
```

A target is therefore not automatically an Observation merely because it has a numeric value. If a target is represented as an Observation in a domain model, its role and provenance must remain explicit.

## Reference

`Reference` is the broad contextual role of an input used for comparison. More specific roles such as baseline, benchmark, target, plan, budget, or forecast should be used when their semantics are known.

```text
Reference
├─ baseline
├─ benchmark
├─ target
├─ plan
├─ budget
├─ forecast
└─ prior period / prior version
```

These roles must not be collapsed into a generic `reference_value` when the distinction affects interpretation.

## Plan and forecast versions

A Plan or Forecast may be revised over time.

For example:

```text
Plan v1
Plan v2
Forecast F1
Forecast F2
Actual A1
```

A comparison must identify the intended version or reference context.

`Actual - Plan` is incomplete as a semantic description if it is unclear whether the comparison uses the original approved plan, the latest revised plan, or another plan version.

## Baseline versus prior value

A prior value is defined by temporal ordering; a baseline is defined by its role as an evaluation reference.

```text
prior = earlier observation/result
baseline = designated reference
```

They may happen to be the same value, but neither concept implies the other.

## Benchmark versus target

A benchmark describes a comparator used for assessment. A target describes an intended outcome.

```text
Benchmark
  = how performance compares with a reference

Target
  = what performance is intended to achieve
```

An organization may set a target equal to a benchmark, but that is a separate business decision.

## Baseline versioning

A baseline may be immutable for a defined planning or measurement context even when later references are revised.

For example:

```text
Approved Plan v1 = baseline
Reforecast v2    = later reference
Actual           = observed outcome
```

Replacing the baseline silently with the latest forecast changes the meaning of historical variance analysis and therefore requires an explicit semantic decision.

## Comparison context

S95 defines comparison results as derived outputs. S96 adds that the reference role is part of the comparison context.

A useful conceptual structure is:

```text
Comparison Context
├─ subject scope
├─ property / phenomenon
├─ observation side
├─ reference side
├─ reference role
├─ temporal context
├─ version / revision
└─ comparison operation
```

This context may be materialized by an application without modifying the Observation primitive.

## Reference may be non-observational

Not every comparison reference is an Observation.

Examples include:

```text
fixed service-level target
policy threshold
contractual limit
standard cost
business rule
```

These may be domain rules or reference values rather than observations of a real-world event.

## Plan / Actual / Forecast semantics

SCM comparison commonly uses:

```text
Actual vs Plan
Actual vs Forecast
Actual vs Budget
Actual vs Target
Forecast vs Prior Forecast
```

Each comparison should preserve the semantic role and version of the reference.

For example:

```text
Actual demand
    vs
Forecast issued 2026-08-01 for week 2026-W33
```

is more precise than an unqualified `Actual vs Forecast`.

## Reference quality and uncertainty

S93 applies to reference values as well as observations where applicable. A benchmark or forecast can have its own uncertainty, provenance, and quality characteristics.

A reference does not become authoritative merely because it is labeled `baseline` or `benchmark`.

## No automatic baseline selection

S96 does not define universal rules such as:

```text
baseline = previous value
baseline = first observation
baseline = latest forecast
baseline = approved plan
```

The selection rule belongs to the applicable business, planning, analytical, or domain contract.

## No mandatory reference fields

S96 does not add fields such as:

```text
baseline_id
benchmark_id
reference_type
target_value
plan_version
```

to the canonical Observation primitive.

These belong to comparison context, reference entities, planning semantics, or domain-specific contracts.

## Non-goals

S96 does not define a universal planning-version model, benchmark registry, target-management system, KPI catalog, budgeting standard, or variance-reporting framework.
