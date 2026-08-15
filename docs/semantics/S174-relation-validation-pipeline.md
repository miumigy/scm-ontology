# S174 — Canonical Relation Validation Pipeline

S174 provides one entry point for validating a typed canonical relation.

```text
predicate + subject type + object type
                 ↓
        validate_relation()
                 ↓
       RelationValidationResult
          ├─ PASS
          ├─ REVIEW
          └─ EXTENSION
```

## Semantics

- `PASS`: the relation matches the current canonical vocabulary and typing contract.
- `REVIEW`: the predicate is canonical, but the supplied types do not satisfy the current contract.
- `EXTENSION`: the predicate is not currently canonical.

Neither REVIEW nor EXTENSION asserts that source data is false. They identify compatibility or coverage gaps.

S174 intentionally does not perform automatic ontology extension, subtype inference, coercion, or graph mutation.
