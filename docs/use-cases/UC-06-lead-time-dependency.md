# S243 — UC-06 Lead-Time Dependency

## Business question

Which explicitly represented lead-time dependency affects the timing of an SCM activity, flow, or supply relationship?

## Canonical intent

Trace a represented lead-time fact to the relationship or activity whose timing it affects.

## Expected path

```text
Activity / Flow / Supply Relationship
        ↓ has_lead_time
Lead-Time Fact
        ↓ affects
Timing Dependency
```

## M5 validation contract

- Canonical concepts: activity/flow/supply relationship, lead-time fact, timing dependency
- Canonical predicates: `has_lead_time`, `affects`
- Path query: focal SCM relationship → lead-time fact → affected timing dependency
- Constraint: requested activity, flow, or timing context must match explicitly when specified
- Expected result: matched lead-time dependency path(s) or explicit `no_match`
- Evidence: source references supporting the lead-time fact
- Explanation: deterministic timing-dependency trace
- Confidence: derived from explicit factors only
- Semantic gap: classify missing temporal semantics before proposing ontology changes

## Canonicality test

ERP routing lead times, WMS processing-time fields, TMS transit-time estimates, and planning-system calendar parameters are adapter-level representations unless independently justified as canonical SCM semantics.

A lead-time fact must not be confused with a system-specific scheduling parameter.

## Acceptance

The use case passes when represented lead-time dependencies can be queried reproducibly without inventing missing temporal facts and without graph mutation.
