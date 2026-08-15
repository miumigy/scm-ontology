# S149 — Provenance / Epistemic Schema

S149 promotes the S103 epistemic and S104 provenance semantics into the machine-readable layer.

## Epistemic status

```text
Fact
Observation
Measurement
Estimate
Prediction
Inference
Assumption
Hypothesis
Unknown
```

These statuses describe what is known and how it is known. They must not be collapsed into a single confidence score.

```text
Fact ≠ Estimate
Estimate ≠ Prediction
Prediction ≠ Actual
Observation ≠ Inference
Unknown ≠ Zero
```

Confidence is optional metadata on an assertion; it does not redefine the assertion's epistemic status.

## Evidence

Evidence is a first-class reference to a source-backed support, contradiction, or context for an assertion.

```text
Source
  ↓
Evidence
  ↓
Epistemic Assertion
```

Evidence can retain observation time and source authority.

## Provenance

Provenance captures lineage for a semantic assertion or value:

```text
Source(s)
   ↓
Transformation / Derivation Rule
   ↓
Provenance Assertion
   ↓
Canonical Assertion
```

Existing provenance primitives remain compatible; S149 adds explicit assertion-level provenance without replacing them.

## Temporal compatibility

Evidence can carry observation time, while assertions can be linked to temporal assertions from S148. Recording when evidence was obtained is not the same as the validity time of the asserted fact.

## Non-goals

S149 does not infer truth from confidence, choose a probabilistic framework, or permit AI-generated inference to be serialized as Fact without an explicit epistemic transition.
