# S170 — Typed Relation Instance Validation

S170 applies the S169 domain/range contracts to concrete relation instances.

```text
Relation Type
    ↓
Domain / Range Contract
    ↓
Typed Relation Instance
    ↓
Validation
```

A valid instance must use a subject type from the predicate domain and an object type from its range.

## Boundary

Validation failure means the instance does not satisfy the current canonical typing contract. It does not prove that the source data is false; mapping or ontology extension may be required.

S170 does not add subclass inference, coercion, cardinality, inverse generation, or business-process inference.
