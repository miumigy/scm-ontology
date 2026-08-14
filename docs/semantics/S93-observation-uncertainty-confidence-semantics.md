# S93 — Observation Uncertainty & Confidence Semantics

S93 defines the semantic boundary between an Observation and statements about its uncertainty, confidence, precision, accuracy, or reliability.

## Canonical decision

Uncertainty and confidence are not mandatory attributes of the canonical Observation primitive.

```text
Observation
├─ observation_id
├─ observed_at
└─ subject_id
```

Quality, uncertainty, and epistemic metadata belong to the surrounding measurement, evidence, provenance, derivation, or data-quality layer.

## Same value, different epistemic status

The same value may have materially different epistemic meanings:

```text
inventory = 120
```

may be:

```text
directly measured
estimated
imputed
reconciled
model-derived
reported by an external source
```

These should not be collapsed into a single generic confidence number.

## Uncertainty versus confidence

S93 keeps these concepts distinct.

```text
Uncertainty
  = characterization of the possible variation or limitation
    surrounding a value or measurement

Confidence
  = degree of belief or assurance associated with a result
    under a specified method or interpretation
```

A confidence score is not automatically an uncertainty interval, and an uncertainty interval is not automatically a probability of correctness.

## Precision versus accuracy

Precision and accuracy are also distinct:

```text
Precision
  = degree of repeatability / fineness of measurement representation

Accuracy
  = closeness to an accepted or reference value
```

A value can be highly precise but systematically inaccurate.

S93 therefore does not use `precision`, `accuracy`, and `confidence` interchangeably.

## Reliability

Reliability is contextual and may describe the trustworthiness of a source, method, instrument, process, or result over a defined context.

```text
source reliability
measurement reliability
process reliability
result confidence
```

These are not necessarily properties of the Observation identity itself.

## Directly observed versus derived

S92 established that estimated or imputed results require explicit derivation/provenance semantics.

S93 extends that boundary:

```text
Direct observation
    ↓
Observation

Derived / estimated result
    ↓
Derivation
    ↓
Observation or domain result
```

A derived value may carry uncertainty introduced by the derivation method, while the input Observations retain their own uncertainty semantics.

## Uncertainty propagation

When observations are aggregated or transformed, uncertainty may need to be propagated according to the applicable domain or statistical method.

For example:

```text
O1 ± u1
O2 ± u2
     ↓ aggregation
O3 ± u3
```

S91 establishes aggregation as derivation. S93 does not prescribe how `u3` is calculated; the method belongs to the applicable measurement/statistical domain.

## Evidence and Claim boundary

Uncertainty about an Observation does not automatically make the Observation false, nor does high confidence automatically make it a Claim.

```text
Observation
    │
    ├── quality / uncertainty metadata
    │
    └── may provide Evidence
             │
             ▼
           Claim
```

Evidence assessment may incorporate uncertainty, provenance quality, source authority, and derivation characteristics.

## Missingness versus uncertainty

S92 distinguishes missing observations from observed zero values. S93 adds that missingness is not itself a numerical uncertainty interval.

```text
missing
    ≠
unknown
    ≠
observed value with uncertainty
```

For example:

```text
inventory = 120 ± 5
```

is an observed/estimated result with explicit uncertainty semantics, while:

```text
inventory = unknown
```

does not provide a numerical estimate at all.

## Confidence scores

An implementation may expose a confidence score, probability, interval, quality grade, or other metric, but its meaning must be defined by the method and domain.

A bare value such as:

```text
confidence = 0.8
```

is not semantically sufficient without knowing what the score measures and how it was produced.

## No mandatory quality fields

S93 does not add mandatory fields such as:

```text
confidence
uncertainty
precision
accuracy
reliability
quality_score
```

to Observation.

Such information may be represented through measurement metadata, provenance, evidence records, derivation metadata, data-quality models, or domain-specific contracts.

## Non-goals

S93 does not define a universal uncertainty model, confidence scale, probability semantics, statistical error-propagation algorithm, measurement-quality standard, reliability score, or data-quality framework.
