# S175 — Relation Validation Contract

S175 consolidates the relation-validation contract after S174's API correction.

The canonical pipeline is:

```text
predicate_ref
    ↓
canonical predicate registry
    ↓
domain/range constraint
    ↓
RelationValidationResult
    ├─ PASS
    ├─ REVIEW
    └─ EXTENSION
```

`PASS` means the predicate is canonical and the supplied direct subject/object types satisfy its current domain/range contract.

`REVIEW` means the predicate is canonical but the current typing contract cannot validate the instance. It does not assert that source data is false.

`EXTENSION` means the predicate is not currently part of the canonical vocabulary. It is an extension candidate, not an automatic ontology mutation.

S175 does not introduce graph mutation, automatic ontology extension, or new inference rules.
