# S245 — UC-08 Demand / Supply Alignment

## Business question

Which explicitly represented supply relationships correspond to a given demand or service requirement?

## Canonical intent

Trace a demand-side requirement to the supply relationship that explicitly serves it, without treating planning quantities or forecasts as canonical truth unless represented as such.

## Expected path

```text
Demand / Service Requirement
        ↓ demanded_by
Supply Relationship
        ↓ supplied_by
Supply Entity
```

## M5 validation contract

- Canonical concepts: demand/service requirement, supply relationship, supply entity
- Canonical predicates: `demanded_by`, `supplied_by`
- Path query: focal demand/service context → supply relationship → supply entity
- Constraint: requested demand, service, or supply entity must match explicitly when specified
- Expected result: matched alignment path(s) or explicit `no_match`
- Evidence: source references supporting demand and supply relationships
- Explanation: deterministic demand/supply alignment trace
- Confidence: derived from explicit factors only
- Semantic gap: classify missing demand/supply semantics before proposing ontology changes

## Canonicality test

Forecast values, MRP proposals, ERP planned orders, APS recommendations, and S&OP workbook fields are representations or derived planning artifacts unless independently justified as canonical SCM semantics.

A planning recommendation must not silently become a canonical supply fact.

## Acceptance

The use case passes when explicit demand/supply relationships can be queried reproducibly without promoting planning recommendations to canonical truth and without graph mutation.
