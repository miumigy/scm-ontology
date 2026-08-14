# S92 — Observation Sampling & Coverage Semantics

S92 defines the semantic boundary between an Observation and the absence, incompleteness, or limitation of observations.

## Canonical decision

The absence of an Observation does not by itself mean zero, false, unchanged, or unknown in the domain.

```text
Observed
    ≠ Not Observed
    ≠ Missing
    ≠ Unknown
    ≠ Zero
```

The canonical Observation primitive remains unchanged:

```text
Observation
├─ observation_id
├─ observed_at
└─ subject_id
```

Sampling, coverage, missingness, and estimation semantics belong to the surrounding domain, provenance, or data-quality layer.

## Zero is an observation

A zero value must be explicitly represented when zero is the observed value.

```text
inventory_level = 0
```

is semantically different from:

```text
no inventory observation available
```

The latter does not establish the former.

## Missing observation

Consider:

```text
10:00 inventory = 100
11:00 no observation
12:00 inventory = 80
```

S92 does not permit an implementation to infer:

```text
11:00 inventory = 90
```

merely from the surrounding observations.

Interpolation, carry-forward, smoothing, or other imputation may be applied by an explicit domain/data-quality process, producing a derived result with appropriate provenance.

## Sampling

A source may observe a subject periodically:

```text
10:00
11:00
12:00
13:00
```

The sampling schedule is not itself an attribute of the canonical Observation. It belongs to the source, measurement process, dataset, or domain observation protocol.

A sampling process may define expected observation opportunities, but an expected opportunity is not equivalent to an actual Observation.

## Coverage

Coverage describes which portion of the relevant domain, population, time range, or subject set is represented by available observations.

Examples include:

```text
subjects covered = 95% of warehouses
time covered = 22 of 24 hours
records covered = 98% of expected records
```

Coverage information must not be inferred solely from the existence of one or more Observation instances unless the relevant sampling/domain rules are known.

## Partial observation

An Observation may describe only part of a domain object or population.

For example:

```text
Region-R inventory observation
  covers warehouses A, B, C
```

does not establish inventory for warehouses D and E.

The scope and coverage of an observation are domain semantics and should be represented explicitly where required.

## Unknown versus missing

S92 keeps two concepts distinct:

```text
Missing
  = an expected or requested observation/value is not available

Unknown
  = the value cannot currently be established
```

A missing source record may lead to an unknown domain value, but the two concepts are not logically identical.

Neither should be silently converted to zero.

## Delayed observations

A delayed Observation remains an Observation of its domain time.

For example:

```text
observed_at = 10:00
recorded_at = 10:20
```

The delay does not change `observed_at` to 10:20. S86 governs the distinction between domain observation time and recording/ingestion time.

## Estimated and imputed values

An estimated or imputed value is not automatically equivalent to a directly observed value.

For example:

```text
O1 = directly observed inventory at 10:00
I1 = imputed inventory at 11:00
O2 = directly observed inventory at 12:00
```

`I1` should carry explicit derivation/provenance semantics identifying that it was inferred rather than directly observed.

The inference process may use O1 and O2, but S92 does not prescribe a particular imputation algorithm.

## Sampling and State inference

S89 establishes that State is distinct from Observation. S92 adds that gaps in observations must not automatically become State continuity.

```text
Observation at T1
      ↓
missing interval
      ↓
Observation at T2
```

does not by itself prove that a State remained unchanged throughout the interval.

A continuity assumption must be an explicit domain rule.

## Coverage and aggregation

S91 establishes that aggregation is derivation and requires semantic compatibility. S92 adds that an aggregate must not be interpreted as full-population coverage unless its input scope and coverage justify that interpretation.

For example:

```text
100 of 120 warehouses observed
```

must not automatically become:

```text
all 120 warehouses observed
```

nor should a sum of the 100 observed warehouses be represented as the full-network inventory without an explicit coverage/estimation semantic.

## No mandatory coverage fields

S92 does not add mandatory `sampling_rate`, `coverage`, `missing`, `is_estimated`, or `is_imputed` fields to the canonical Observation primitive.

Implementations may represent these semantics in dataset metadata, provenance, derivation records, quality models, or domain-specific contracts.

## Non-goals

S92 does not define a universal missing-data taxonomy, statistical sampling standard, imputation algorithm, data-quality score, coverage metric, or uncertainty model.
