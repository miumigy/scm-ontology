# S173 — Structured Relation Validation Result

S173 makes relation validation outcomes explicit and inspectable.

## Result model

```text
RelationValidationResult
├─ predicate_ref
├─ status
├─ reason
├─ subject_type
├─ object_type
├─ domain_ok
└─ range_ok
```

The status remains deliberately coarse:

- `PASS` — canonical typing contract is satisfied.
- `REVIEW` — the assertion does not satisfy the current contract and requires review.
- `EXTENSION` — the predicate is outside the canonical vocabulary.
- `ERROR` — reserved for future processing failures.

## Important boundary

A `REVIEW` or `EXTENSION` result is not a statement that the source fact is false. It is a validation outcome about compatibility with the current Canonical Model.

The result preserves subject/object type information and the two validation dimensions so downstream Mapping, Graph ingestion, and QA tooling can make the next decision without losing diagnostic context.
