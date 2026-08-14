# S90 — Observation Correction & Revision Semantics

S90 defines how an Observation is corrected, superseded, invalidated, or retracted without destroying the identity of the original observation.

## Canonical decision

An Observation instance is treated as historically identifiable information. A correction does not silently mutate the semantic identity of the original Observation.

```text
Observation O1
  value = 120

Observation O2
  value = 118

O2 ── corrects ──→ O1
```

O1 and O2 remain distinct Observation instances.

The canonical Observation primitive is unchanged:

```text
Observation
├─ observation_id
├─ observed_at
└─ subject_id
```

Correction and revision are represented as relationships or application-layer semantics, not as additional mandatory fields on Observation.

## Correction versus derivation

Correction and derivation are related but distinct.

```text
Derivation
  = produces an artifact/observation from inputs

Correction
  = identifies a later observation as correcting an earlier observation
```

A corrected Observation may itself be derived, but derivation alone does not imply correction.

## Original observation identity

Consider:

```text
O1: inventory = 120
O2: inventory = 118
```

If O2 corrects O1:

```text
O2 ── corrects ──→ O1
```

The system must not rewrite O1 into 118. Preserving O1 allows consumers to reconstruct what was previously observed or reported and why it was later superseded.

## Correction is not deletion

A correction does not mean that the original Observation never existed.

```text
O1
 │
 │ corrected_by
 ▼
O2
```

The original may remain queryable subject to application retention, privacy, and governance policies.

## Revision versus correction

S90 distinguishes the concepts without requiring a universal status enum.

### Correction

A later Observation is explicitly identified as correcting an earlier Observation because the earlier information was erroneous, incomplete, or otherwise inaccurate for its intended semantics.

```text
O2 corrects O1
```

### Supersession

A later Observation replaces an earlier one for an application purpose without necessarily asserting that the earlier Observation was factually erroneous.

```text
O2 supersedes O1
```

For example, a refreshed operational snapshot may supersede an earlier snapshot while both remain historically valid representations of their respective observation events.

### Invalidation

An Observation may be invalidated when it must no longer be treated as valid for a specified application or semantic purpose.

Invalidation is not necessarily a statement that the Observation never occurred.

### Retraction

Retraction indicates that an Observation is withdrawn from use, for example because its provenance or authority is no longer acceptable. Retraction does not require rewriting the historical identity of the Observation.

These meanings must not be collapsed into a single generic `updated` flag.

## Temporal distinction

Correction time is not observation time.

Example:

```text
O1
  observed_at = 10:00
  value = 120

O2
  observed_at = 10:00
  generated/recorded = 10:05
  value = 118
```

O2 may correct O1's interpretation of the same domain observation time. The later correction event does not change O1's original `observed_at`.

## State implications

S89 establishes that State is distinct from Observation. A correction may change which Observations are used to derive a State, but it does not mutate the identity of the source Observation.

```text
O1 ──┐
     ├─ state derivation → S1
O2 ──┘
```

An application may recompute S1 after a correction, but that recomputation belongs to State/derivation semantics.

## Evidence and Claim implications

If an Observation was used as Evidence for a Claim and is later corrected, invalidated, or retracted, the application must evaluate the affected Evidence and Claim relationships explicitly.

```text
Observation O1
      │ evidence
      ▼
Claim C1

O2 corrects O1
```

S90 does not automatically invalidate C1. Epistemic impact assessment is a separate semantic process.

## No mandatory status field

S90 does not add a mandatory `status`, `version`, `revision`, `corrected_by`, or `supersedes` field to the Observation primitive.

Implementations may materialize these relationships in a graph, relational model, event log, or application API while preserving the canonical semantic boundary.

## Non-goals

S90 does not define a universal revision-control protocol, audit-log schema, retention policy, status enumeration, automatic claim retraction algorithm, or database update strategy.
