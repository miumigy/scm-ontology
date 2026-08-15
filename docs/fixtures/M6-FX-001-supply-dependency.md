# M6-FX-001 — Supply Dependency Chain

## Purpose

Executable canonical graph fixture for UC-01 Supply Dependency and UC-02 Site Dependency.

## Graph

```text
Material M-001
    ↓ supplied_by
Supplier S-001
    ↓ located_at
Site SITE-001
```

The fixture includes evidence references on both canonical edges and two deterministic business questions.

## M6 invariants

- read-only reasoning
- no inferred canonical fact creation
- no enterprise-specific semantics in the canonical graph

## Expected validation

1. Identify Supplier Alpha as the supplier of Resin A.
2. Identify Alpha Plant as the physical site supporting Resin A's supply.
3. Preserve evidence references for both relationships.
