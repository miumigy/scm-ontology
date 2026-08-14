# S97 — Observation Threshold & Tolerance Semantics

S97 defines how thresholds, tolerances, limits, targets, and alert/control rules are applied to Observations or derived comparison results.

## Canonical decision

A threshold or tolerance is an evaluation rule, not an intrinsic property of an Observation.

```text
Observation / Comparison Result
          │
          ▼
Evaluation Rule
          │
          ├─ threshold
          ├─ tolerance
          ├─ limit
          └─ control / alert rule
          │
          ▼
Evaluation Result
```

The canonical Observation primitive remains unchanged.

## Difference versus evaluation

S95 defines the numerical comparison result. S97 defines the subsequent evaluation.

```text
Actual = 102
Target = 100

Difference = +2

Tolerance = ±5

Evaluation = within tolerance
```

The value `+2` and the judgment `within tolerance` are different semantic artifacts.

## Threshold

A threshold defines a boundary at which an evaluation condition changes.

Examples:

```text
inventory < 20
service_level < 95%
lead_time > 7 days
```

A threshold may be one-sided or multi-sided depending on the rule.

## Tolerance

Tolerance defines an accepted range around a reference or expected value.

```text
Target = 100
Tolerance = ±5
Accepted range = [95, 105]
```

Tolerance is contextual to a reference and evaluation rule. It is not the same as measurement uncertainty from S93.

## Measurement uncertainty versus tolerance

These concepts must remain distinct.

```text
Measurement uncertainty
  = limitation/variation associated with the measured or derived value

Tolerance
  = acceptable deviation defined by a business, engineering,
    contractual, or operational rule
```

For example:

```text
Actual = 102 ± 2
Target = 100
Tolerance = ±5
```

The `±2` and `±5` have different meanings even though both are intervals.

## Limit

A limit is a boundary imposed by a rule, specification, policy, contract, or operating condition.

Examples:

```text
maximum inventory = 500
minimum service level = 95%
maximum lead time = 7 days
```

A limit does not necessarily express a desired target. It may express a hard constraint.

## Target

S96 defines Target as an intended or desired reference. S97 distinguishes it from the tolerance around that target.

```text
Target = desired value
Tolerance = acceptable deviation from target
Limit = boundary that must not be crossed
```

A target may have an associated tolerance, but it does not inherently imply one.

## Alert and control rules

An alert rule transforms an evaluated condition into an operational signal.

```text
Observation
    ↓
Evaluation
    ↓
Condition = breach
    ↓
Alert / Exception
```

The alert itself is not the Observation and should not mutate it.

Control rules may additionally determine an action, escalation, or workflow.

## Directionality

Evaluation rules must specify direction where relevant.

For example:

```text
inventory > upper_limit → breach
inventory < lower_limit → breach
```

A symmetric tolerance rule and a one-sided threshold are not interchangeable.

## Absolute versus relative tolerance

Tolerance may be absolute or relative.

```text
absolute tolerance = ±5 units
relative tolerance = ±5%
```

They should not be treated as equivalent without an explicit rule.

For a target of 100:

```text
±5 units → [95, 105]
±5%       → [95, 105]
```

but for a target of 1,000:

```text
±5 units → [995, 1005]
±5%      → [950, 1050]
```

The tolerance representation must therefore preserve its basis.

## Evaluation result

An evaluation result may be represented conceptually as:

```text
Evaluation Result
├─ input
├─ rule
├─ condition
└─ outcome
```

Possible outcomes include:

```text
within tolerance
warning
breach
critical breach
not evaluable
```

S97 does not prescribe a universal outcome vocabulary.

## Not evaluable

A rule cannot be evaluated when required semantic inputs are missing or incompatible.

For example:

```text
Actual available
Target unavailable
```

must not automatically become `breach`, `within tolerance`, or `zero variance`.

S92's missingness semantics and S94's comparability semantics remain applicable.

## Time-varying thresholds

Thresholds and tolerances may themselves vary by:

```text
time
season
SKU
site
customer
contract
operating mode
planning version
```

The applicable rule context must therefore be identifiable when historical evaluation results are reconstructed.

## Rule versioning

Changing a threshold can change evaluation outcomes without changing the underlying Observation.

```text
Observation O1 = 102

Rule v1: tolerance ±5 → within tolerance
Rule v2: tolerance ±1 → breach
```

The difference is in the evaluation rule, not in O1.

Historical analytics should preserve the relevant rule/version context when reproducibility matters.

## Relationship to State

An evaluation result may contribute to State or trigger a state transition, but the evaluation itself is not automatically a State.

```text
Observation
   ↓
Evaluation
   ↓
Exception / State transition
```

Domain rules determine whether and how the evaluation affects State.

## Relationship to Evidence and Claim

An evaluation result may support an operational Claim or decision, but it does not become a Claim merely because it says `breach`.

```text
Observation
   ↓
Evaluation
   ↓
Evidence / operational signal
   ↓
Claim / Decision
```

The epistemic and operational layers remain distinct.

## No mandatory threshold fields

S97 does not add fields such as:

```text
threshold
tolerance
limit
alert_level
rule_id
```

to the canonical Observation primitive.

These belong to evaluation rules, reference semantics, policy/configuration, or domain-specific contracts.

## Non-goals

S97 does not define a universal alert taxonomy, SLA standard, statistical control-chart method, tolerance-calculation algorithm, workflow engine, policy language, or exception-management framework.
