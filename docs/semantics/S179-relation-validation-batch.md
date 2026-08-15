# S179 — Batch Relation Validation

S179 adds a small batch API over the canonical relation validation pipeline.

```text
many typed relations
        ↓
validate_relations()
        ↓
ordered RelationValidationResult[]
```

Each relation is validated independently. One `REVIEW` or `EXTENSION` result does not suppress or mutate other results.

The API preserves input order and performs no graph mutation, automatic ontology extension, or cross-relation inference.
