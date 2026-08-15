# S242 — UC-05 Capacity Dependency

## Business question

Which capacity resource or physical capability is required to fulfill a supply-chain activity?

## Canonical intent

Trace an explicitly represented requirement from an activity or operation to the capacity resource that provides it.

## Expected path

```text
Activity / Operation
        ↓ requires_capacity
Capacity Requirement
        ↓ provided_by
Capacity Resource
```

## M5 validation contract

- Canonical concepts: activity/operation, capacity requirement, capacity resource
- Canonical predicates: `requires_capacity`, `provided_by`
- Path query: focal activity → capacity requirement → capacity resource
- Constraint: requested resource or capability must match explicitly when specified
- Expected result: matched capacity dependency path(s) or explicit `no_match`
- Evidence: source references supporting the capacity requirement and resource relationship
- Explanation: deterministic capacity dependency trace
- Confidence: derived from explicit factors only
- Semantic gap: classify missing capacity semantics before proposing ontology changes

## Canonicality test

ERP work-center IDs, APS resource codes, machine IDs, labor-category codes, and vendor-specific capacity identifiers are adapter-level representations unless independently justified as canonical SCM semantics.

## Acceptance

The use case passes when capacity dependency can be queried reproducibly from canonical facts without inferring unrepresented capacity and without graph mutation.
