# S241 — UC-04 Inventory Dependency

## Business question

Where is inventory positioned, and which downstream service or demand context does that inventory support?

## Canonical intent

Trace an explicitly represented inventory position to the physical node where it is held and to an explicitly represented service or demand relationship.

## Expected path

```text
Material / Product
      ↓ stocked_at
Inventory Position / Stock
      ↓ serves
Demand / Service Context
```

The physical inventory location is represented separately from the inventory quantity/state itself.

## M5 validation contract

- Canonical concepts: material/product, inventory position, physical node, demand/service context
- Canonical predicates: `stocked_at`, `serves`
- Path query: focal inventory/product → stock position → service context
- Constraint: requested node or service context must be matched explicitly when specified
- Expected result: matched dependency path(s) or explicit `no_match`
- Evidence: source references supporting inventory and service relationships
- Explanation: deterministic inventory dependency trace
- Confidence: derived from explicit factors only
- Semantic gap: classify missing inventory/service semantics before proposing ontology changes

## Canonicality test

ERP material-document numbers, WMS bin IDs, batch-system identifiers, and product-specific stock fields are adapter-level representations unless independently justified as canonical SCM semantics.

## Acceptance

The use case passes when inventory dependency can be queried reproducibly from canonical facts without inferring inventory that is not represented and without graph mutation.
