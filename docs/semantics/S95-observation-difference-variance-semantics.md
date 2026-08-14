# S95 — Observation Difference & Variance Semantics

S95 defines the semantic boundary between comparable Observations, comparison operations, and derived difference/variance results.

## Canonical decision

A numerical difference is a derived result of an explicitly defined comparison operation. It is not an intrinsic property of either Observation.

```text
Comparable Observation A ─┐
                          ├─ comparison operation ─→ Result R
Comparable Observation B ─┘
```

The canonical Observation primitive remains unchanged.

## Difference

A difference is an ordered operation whose sign depends on the declared operand order.

```text
A - B = +20
```

is not semantically equivalent to:

```text
B - A = -20
```

Therefore a comparison result must preserve the operation or operand roles when sign interpretation matters.

## Variance is overloaded

S95 explicitly distinguishes SCM variance from statistical variance.

### SCM / business variance

```text
Actual - Plan
Actual - Forecast
Actual - Target
Current - Prior
```

may be called a variance in business contexts. Its meaning depends on the declared baseline and direction.

### Statistical variance

Statistical variance is a dispersion measure derived from a population or sample according to a statistical definition.

```text
Var(X)
```

It must not be inferred from a two-value business difference merely because both are called “variance”.

## Directionality

The semantic roles of operands should be explicit where interpretation depends on them.

```text
Actual = 120
Plan   = 100

Actual - Plan = +20
```

versus:

```text
Plan - Actual = -20
```

Both arithmetic results are valid, but they express different business semantics.

## Percentage change

Percentage change is not identical to absolute difference.

```text
(A - B) / B × 100
```

requires a declared baseline `B` and a denominator that is semantically valid for the operation.

A zero or unsuitable denominator requires explicit handling rather than silent substitution.

## Ratio

A ratio is an ordered relation such as:

```text
A / B
```

It is distinct from percentage change even when the two are mathematically related.

For example:

```text
A / B = 1.2
percentage change = 20%
```

The result semantics and units differ.

## Error and bias

Forecast or estimation contexts require explicit role semantics.

For example:

```text
Forecast error = Actual - Forecast
```

is one possible convention. Another application may define:

```text
Forecast error = Forecast - Actual
```

S95 does not mandate one sign convention globally. The operation and operand roles must be explicit.

Bias is an aggregate property of a collection of errors or deviations under a defined method; it is not synonymous with a single difference.

## Absolute error

Absolute error removes direction:

```text
|Actual - Forecast|
```

This is distinct from signed forecast error and should not be used interchangeably with it.

## Comparability prerequisite

S94 establishes comparability as a prerequisite for meaningful comparison. S95 does not allow a mathematically computable result to be treated as semantically valid merely because subtraction or division is technically possible.

```text
numeric computability
    ≠ semantic validity
```

## Units of derived results

Difference results generally retain the compatible quantity kind and unit of the operands.

Ratios and percentage changes are dimensionless, subject to the semantics of the operation.

For example:

```text
120 units - 100 units = 20 units
120 units / 100 units = 1.2
(120 - 100) / 100 = 20%
```

The result type should reflect these differences.

## Temporal comparison

Comparisons across time must respect S94 temporal comparability semantics.

A difference between:

```text
inventory at 10:00
inventory at 11:00
```

may represent a change over time, while a difference between:

```text
monthly average inventory
inventory at 11:00
```

requires an explicit transformation before interpretation.

## Uncertainty and significance

S93 establishes uncertainty as a separate semantic layer. A numerical difference does not automatically establish a materially meaningful difference.

```text
A = 120 ± 5
B = 123 ± 5
A - B = -3
```

The arithmetic result is valid if the inputs are comparable, but significance or confidence in the difference requires additional domain/statistical semantics.

## Result is not an Observation by default

A comparison result may be represented as a derived Observation when it has a valid observation subject, property, time semantics, and provenance. However, the arithmetic operation itself does not automatically turn the result into an Observation.

```text
Comparison Result
    ≠ Observation
```

unless the applicable domain contract explicitly represents it as such.

## No mandatory comparison fields

S95 does not add fields such as:

```text
baseline_id
comparison_type
variance
error
ratio
```

to the canonical Observation primitive.

These belong to comparison/derivation result semantics.

## Non-goals

S95 does not define a universal variance sign convention, statistical variance estimator, forecast-error standard, significance test, normalization engine, or KPI catalog.
