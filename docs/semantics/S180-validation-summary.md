# S180 — Validation Summary

S180 adds a deterministic summary over batch relation-validation results.

```text
RelationValidationResult[]
        ↓
summarize_validation()
        ↓
PASS / REVIEW / EXTENSION counts
```

The summary is observational only. It does not alter validation results, perform inference, mutate the graph, or automatically promote extensions.
