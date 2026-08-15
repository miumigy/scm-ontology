# S238 — UC-01 Supply Dependency

## Business question

Which upstream supply relationships support a given product or material?

## Canonical intent

Trace an existing dependency path from a focal product/material to its supplying entity.

## Expected path

```text
Product / Material
      ↓ depends_on
Supply Entity
      ↓ supplied_by
Supplier / Source
```

The exact predicates must be validated against the canonical model. This use case must not introduce vendor-specific concepts.

## M5 validation contract

- Canonical concepts: product/material, supply entity, supplier/source
- Canonical predicates: `depends_on`, `supplied_by`
- Path query: focal entity → dependency predicates
- Constraint: path must terminate at the requested supplier/source when specified
- Expected result: matched path(s) or explicit `no_match`
- Evidence: source references supporting the relationships
- Explanation: deterministic path/evidence trace
- Confidence: derived only from explicit factors
- Semantic gap: classify missing concepts/predicates before changing the ontology

## Acceptance

The use case passes when the same canonical graph and query produce the same result, explanation, and evidence trace without graph mutation.
