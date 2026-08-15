# S218 — Reasoning Result Model

S218 defines the explicit output contract of the reasoning boundary.

```text
Query / Constraint Evaluation
          ↓
    ReasoningResult
      ├─ result_ref
      ├─ status
      ├─ matches
      ├─ evidence
      ├─ explanation
      └─ metadata
```

A result reports evaluated existing facts and their evidence. It does not itself mutate the canonical graph or assert that a result is universally true.
