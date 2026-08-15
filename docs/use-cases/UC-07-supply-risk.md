# S244 — UC-07 Supply Risk

## Business question

Which upstream supply dependencies expose a product or material to explicitly represented supply risk?

## Canonical intent

Trace a multi-hop dependency from a focal product/material through its supplier and physical site, then associate that path with explicitly represented risk information.

## Expected path

```text
Product / Material
      ↓ depends_on / supplied_by
Supplier
      ↓ located_at
Site
      ↓ exposed_to / has_risk
Supply Risk
```

The exact risk predicates must be validated against the canonical model. The use case must not assume that geographic, supplier, or concentration characteristics are themselves risk facts unless represented explicitly.

## M5 validation contract

- Canonical concepts: product/material, supplier, site, supply risk
- Canonical predicates: existing dependency/location predicates plus validated risk predicate(s)
- Path query: focal entity → supplier → site → explicit risk fact
- Constraint: requested risk type, supplier, site, or dependency must match explicitly when specified
- Expected result: matched multi-hop risk path(s) or explicit `no_match`
- Evidence: source references supporting each material relationship and the risk fact
- Explanation: deterministic multi-hop dependency and risk trace
- Confidence: derived from explicit factors only
- Semantic gap: classify missing risk semantics before proposing ontology changes

## Canonicality test

Supplier scores, ERP vendor-risk flags, TMS alerts, external risk-provider ratings, and certification labels are adapter-level evidence unless independently justified as canonical SCM risk semantics.

A risk indicator must not be promoted to canonical truth merely because an external system labels it as high risk.

## Acceptance

The use case passes when at least one representative multi-hop supply-risk scenario can be reasoned over from canonical facts and explicit risk evidence without silently creating risk facts or mutating the graph.
