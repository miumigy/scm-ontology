# S166 — Relation Schema Integration

S166 connects the S165 canonical relation registry to the machine-readable assertion schema.

## Contract

```text
Canonical Relation Registry
          ↓
Canonical predicate vocabulary
          ↓
JSON Schema relationAssertion.predicate_ref
          ↓
Machine validation
```

A relation assertion may use a predicate only from the canonical vocabulary published by S165.

## Boundary

This does not make JSON Schema the source of semantic truth. The S165 relation registry remains the semantic model; the schema mirrors its currently supported predicate vocabulary for interchange validation.

Likewise, vendor-specific predicates remain outside the canonical vocabulary and must be mapped before entering the canonical assertion layer.

## Important limitation

The schema constrains the predicate vocabulary but does not encode domain-specific subject/object typing, inverse materialization, cardinality, or causal inference. Those remain semantic/runtime responsibilities.
