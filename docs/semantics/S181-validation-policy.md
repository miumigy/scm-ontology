# S181 — Validation Disposition Policy

S181 separates validation status from downstream handling policy.

```text
ValidationStatus
    ↓
disposition_for()
    ↓
ACCEPT
REVIEW
EXTENSION_CANDIDATE
```

`PASS` becomes `ACCEPT`, `REVIEW` remains `REVIEW`, and `EXTENSION` becomes `EXTENSION_CANDIDATE`.

This is a policy mapping only. It does not assert source-data truth, mutate the graph, or automatically extend the ontology.
