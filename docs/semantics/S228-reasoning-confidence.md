# S228 — Reasoning Confidence

S228 introduces a transparent confidence model for reasoning results.

Confidence is represented by explicit factors:

- evidence completeness
- source agreement
- path consistency
- determinism

Each factor and the resulting score are bounded to `[0, 1]`. The initial score is the arithmetic mean of the factors.

```text
ConfidenceFactors
      ↓
ReasoningConfidence
```

The confidence score is derived metadata. It is not a canonical fact and does not modify graph truth.
