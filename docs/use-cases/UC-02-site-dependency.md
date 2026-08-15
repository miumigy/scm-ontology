# S239 — UC-02 Site Dependency

## Business question

Which physical site or facility is exposed when a supply dependency is traced upstream?

## Canonical intent

Trace an existing supply relationship from a focal product/material through its supplier to the supplier's physical site.

## Expected path

```text
Product / Material
      ↓ supplied_by
Supplier
      ↓ located_at
Site
```

## M5 validation contract

- Canonical concepts: product/material, supplier, site
- Canonical predicates: `supplied_by`, `located_at`
- Path query: focal entity → supplier → site
- Constraint: path terminates at the requested site when specified
- Expected result: matched site path(s) or explicit `no_match`
- Evidence: source references supporting supplier and site relationships
- Explanation: deterministic relationship/evidence trace
- Confidence: derived from explicit factors only
- Semantic gap: classify missing concepts/predicates before proposing ontology changes

## Canonicality test

The site must be represented semantically as a physical SCM location, not as an SAP plant code, WMS warehouse code, or vendor-specific facility identifier.

## Acceptance

The use case passes when the same canonical graph and query reproducibly identify the same site dependency without graph mutation or vendor-specific semantics.
