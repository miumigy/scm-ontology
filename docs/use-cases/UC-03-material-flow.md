# S240 — UC-03 Material Flow

## Business question

How does a material or product move between physical supply-chain nodes?

## Canonical intent

Trace an explicitly represented movement between physical nodes without inferring an unrecorded shipment.

## Expected path

```text
Material / Product
      ↓ moves
Flow / Movement
      ↓ from
Origin Node
      ↓ to
Destination Node
```

## M5 validation contract

- Canonical concepts: material/product, movement/flow, physical node
- Canonical predicates: `moves`, `from`, `to`
- Path query: focal material/product → movement → origin/destination
- Constraint: origin and destination must match explicitly requested nodes when specified
- Expected result: matched movement path(s) or explicit `no_match`
- Evidence: source references supporting the movement representation
- Explanation: deterministic flow/path trace
- Confidence: derived from explicit factors only
- Semantic gap: classify missing flow semantics before proposing ontology changes

## Canonicality test

Transport-system identifiers, carrier codes, TMS shipment numbers, and route-specific fields are adapter-level representations unless independently justified as canonical SCM concepts.

## Acceptance

The use case passes when existing canonical movement facts can be queried reproducibly without silently creating missing movements or mutating the graph.
