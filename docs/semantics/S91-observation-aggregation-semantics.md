# S91 — Observation Aggregation Semantics

S91 defines how multiple Observations may be aggregated into a new Observation without conflating aggregation with Observation identity.

## Canonical decision

Aggregation is a form of derivation.

```text
Observation O1 ─┐
Observation O2 ─┼─ aggregation activity ─→ Observation O3
Observation O3 ─┘
```

The resulting O3 is a new Observation with its own identity. Aggregation does not mutate or merge the identities of the input Observations.

The canonical Observation remains:

```text
Observation
├─ observation_id
├─ observed_at
└─ subject_id
```

Aggregation semantics belong to the derivation/domain layer.

## Aggregation versus identity

If:

```text
SKU-A @ WH-A = 100
SKU-B @ WH-A = 200
SKU-C @ WH-A = 300
```

are aggregated into:

```text
WH-A total inventory = 600
```

then the total is represented by a new Observation or domain result. It is not the same Observation as any input.

```text
O1 ─┐
O2 ─┼─ sum ─→ O4
O3 ─┘
```

## Aggregation operator

An aggregation activity may specify an operator such as:

```text
sum
average
minimum
maximum
count
weighted_average
percentile
```

S91 does not prescribe a universal operator vocabulary. The operator is part of the derivation semantics and must be interpretable by the consuming domain/application.

## Semantic compatibility

Aggregation is valid only when the input observations are semantically compatible with the chosen operator.

Relevant dimensions may include:

```text
property / phenomenon
unit
quantity kind
subject scope
time semantics
currency
population / sample semantics
```

For example:

```text
inventory(WH-A) = 100 units
inventory(WH-B) = 200 units
→ regional inventory = 300 units
```

may be valid when the target scope is the union of WH-A and WH-B.

By contrast:

```text
temperature(WH-A) = 20 °C
temperature(WH-B) = 30 °C
→ temperature = 50 °C
```

is not a valid simple sum. A meaningful aggregate might instead require an explicitly defined average or weighted average.

## Scope transformation

Aggregation often changes the scope of the subject.

```text
WH-A inventory
WH-B inventory
      │
      │ aggregate
      ▼
Region-R inventory
```

The resulting Observation must identify the appropriate target subject (`Region-R` in this example). It must not encode the source subjects by concatenating identifiers into `subject_id`.

## Temporal compatibility

Aggregation must also respect temporal semantics.

Observations with different `observed_at` values cannot automatically be treated as simultaneous inputs.

For example:

```text
WH-A inventory at 10:00
WH-B inventory at 15:00
```

requires a domain rule before it can be described as a single point-in-time regional inventory observation.

The aggregation process may instead produce a time-window result or another domain-specific temporal object.

## Units and dimensions

Numeric compatibility is not sufficient by itself.

```text
100 kg + 200 kg = 300 kg
```

is dimensionally coherent, while:

```text
100 kg + 200 pieces
```

is not.

Unit conversion may be part of the derivation before aggregation, but S91 does not define a universal conversion engine.

## Aggregation versus simple derivation

S91 treats aggregation as a specialization of derivation rather than as an unrelated primitive.

```text
Derivation
├─ aggregation
├─ reconciliation
├─ transformation
└─ other domain-defined derivations
```

The distinction remains useful at the application layer because aggregation carries additional semantic constraints, especially around scope, units, populations, and temporal alignment.

## Aggregation versus State

An aggregated Observation may later be used to derive or represent a State, but aggregation itself does not create a State.

```text
Observations
   ↓ aggregation
Observation O3
   ↓ optional interpretation
State S1
```

## Aggregation versus Claim

An aggregated Observation is not automatically a Claim.

```text
Aggregation
    → derived Observation

Evidence
    → supports / contradicts Claim
```

An aggregated Observation may subsequently be used as Evidence for a Claim.

## No automatic aggregation

The existence of multiple observations with apparently compatible values does not imply that they should be aggregated. The aggregation operator, target scope, semantic compatibility, and temporal interpretation must be established explicitly by the applicable domain/application rules.

## Non-goals

S91 does not define a universal aggregation operator registry, unit-conversion system, temporal alignment algorithm, hierarchy model, statistical aggregation standard, or KPI catalog.
