# S154 — Temporal / Provenance / Epistemic Integration

S154 connects the cross-cutting dimensions introduced in S103, S104, and S106 without collapsing them into a single status field.

## Canonical pattern

```text
Canonical Assertion
   ├── What is known?      → Epistemic Kind
   ├── When is it valid?   → Temporal Assertion(s)
   └── Why do we trust it? → Provenance
```

Confidence is an additional epistemic qualifier; it does not replace epistemic kind.

## Important boundaries

```text
Fact        ≠ Observation
Observation ≠ Inference
Estimate    ≠ Prediction
Prediction  ≠ Actual
Unknown     ≠ Zero

Effective Time  ≠ Transaction Time
Observation Time ≠ Effective Time
Planned Time    ≠ Actual Time

Provenance ≠ Confidence
Confidence ≠ Truth
```

The `SemanticContext` binds these dimensions to the same assertion and subject while retaining their independent semantics.

## Historical and reasoning implications

A graph consumer can now ask, for one assertion:

- what is being asserted;
- whether it is observed, inferred, estimated, predicted, or unknown;
- when it is semantically valid or observed;
- which provenance supports it;
- what confidence accompanies the epistemic assessment.

This supports evidence-aware reasoning without turning an inference into a historical fact.

## Non-goals

S154 does not implement provenance storage, probabilistic inference, temporal databases, confidence calibration, or a truth-maintenance system. It defines the canonical cross-dimensional contract.
