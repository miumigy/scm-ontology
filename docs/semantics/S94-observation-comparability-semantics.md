# S94 — Observation Comparability Semantics

S94 defines when two Observations may be meaningfully compared and separates comparability from the comparison result itself.

## Canonical decision

Comparability is a semantic relation established by compatibility of the relevant Observation interpretations. It is not implied merely because two Observations contain numeric values.

```text
Observation A ─┐
               ├─ comparability assessment ─→ comparable / not comparable / conditional
Observation B ─┘
```

A comparison result is a separate derived result:

```text
Observation A ─┐
               ├─ comparison operation ─→ Result R
Observation B ─┘
```

The canonical Observation primitive remains unchanged.

## Core comparability dimensions

Depending on the comparison operation, relevant dimensions may include:

```text
subject scope
property / phenomenon
value semantics
unit / quantity kind
time semantics
currency
measurement method
population / sample scope
aggregation level
quality / uncertainty
```

Not every comparison requires every dimension, but the dimensions material to the intended interpretation must be compatible.

## Subject comparability

Subjects need not be identical for every comparison, but their relationship must support the intended operation.

Examples:

```text
WH-A inventory today
WH-A inventory yesterday
```

supports temporal comparison.

```text
WH-A inventory
WH-B inventory
```

may support cross-site comparison if the property and scope are semantically aligned.

A comparison must not silently treat unrelated subjects as interchangeable.

## Property comparability

Observations should concern the same or explicitly comparable property/phenomenon for a direct comparison.

```text
inventory_level = 120
inventory_level = 150
```

is directly comparable under compatible scope and units.

```text
temperature = 20
inventory_level = 150
```

is not a meaningful direct comparison merely because both values are numeric.

## Unit and quantity compatibility

Values expressed in different but convertible units may be comparable after an explicit, valid conversion.

```text
100 kg
220.46 lb
```

may be converted into a common representation before comparison.

Different quantity kinds must not be compared as though unit conversion could make them equivalent.

## Temporal comparability

Time semantics matter.

Examples:

```text
inventory at 10:00
inventory at 11:00
```

may support a time-series comparison.

However:

```text
monthly average inventory
point-in-time inventory
```

are not directly interchangeable without an explicit transformation.

S86's distinction between observation time and recording/ingestion time remains in force.

## Scope and aggregation level

Observations at different hierarchy levels may require transformation before comparison.

```text
Warehouse-A inventory
Region-R inventory
```

should not be directly differenced as though they represent the same scope.

An aggregation or disaggregation process may establish comparability when its semantic rules justify it.

## Currency and economic values

Monetary observations may require compatible currency, valuation basis, price basis, and time context.

For example:

```text
JPY cost
USD cost
```

requires an explicit currency conversion and appropriate exchange-rate semantics before direct numerical comparison.

Nominal and real values should not be silently compared when inflation or valuation basis materially affects the interpretation.

## Measurement method

Two values with the same property and unit may still be conditionally comparable when measurement methods differ.

For example:

```text
sensor measurement
manual count
model estimate
```

may require method-specific qualification before being compared directly.

S93's uncertainty and quality semantics may affect whether a comparison is appropriate or how its result should be interpreted.

## Comparability versus comparison

S94 explicitly separates:

```text
Comparability
  = whether an intended comparison is semantically valid

Comparison
  = an operation performed on comparable inputs

Comparison result
  = derived output such as difference, ratio, variance, or trend
```

Therefore:

```text
A comparable to B
    ≠
A - B
```

The latter is a derived result whose semantics depend on the chosen operation.

## Conditional comparability

Comparability may be conditional rather than binary.

Examples:

```text
comparable after unit conversion
comparable after currency normalization
comparable after aggregation alignment
comparable only for directional ranking
not suitable for absolute difference
```

An implementation may model such conditions outside the canonical Observation primitive.

## Plan, actual, and forecast

SCM commonly compares:

```text
Actual
Plan
Forecast
Budget
Target
Prior period
```

These are not automatically interchangeable observation types. Their semantic roles and time/reference contexts must be aligned before operations such as variance or forecast error are interpreted.

For example:

```text
Actual demand
Forecast demand
```

may support forecast-error analysis when their subject, demand definition, period, scope, and units align.

## Uncertainty and significance

S93 establishes that uncertainty is separate from Observation identity. S94 adds that a numerical difference does not automatically imply a meaningful difference.

For example:

```text
A = 120 ± 5
B = 123 ± 5
```

may produce a numerical difference of 3, while the practical or statistical significance of that difference requires additional domain/statistical semantics.

## No automatic comparability

The presence of two observations with similar labels or numeric values does not establish comparability. The intended comparison and its required semantic dimensions must be explicit enough for the result to be interpretable.

## Non-goals

S94 does not define a universal similarity metric, statistical hypothesis test, variance formula, normalization engine, unit-conversion system, currency conversion service, or KPI catalog.
