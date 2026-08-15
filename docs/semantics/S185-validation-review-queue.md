# S185 — Validation Review Queue

S185 adds a read-only projection for downstream human review.

```text
Validation Results
      ↓
review_queue()
      ↓
REVIEW results only
```

The queue preserves source order and references the existing immutable validation results. It does not reinterpret results, perform inference, mutate the graph, or promote ontology extensions automatically.
