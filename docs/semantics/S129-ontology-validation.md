# S129 — Ontology Validation

## Purpose

S118 established local semantic consistency validation. S129 adds cross-layer invariants for the canonical ontology and its future graph projection.

The validator protects semantic boundaries rather than judging business correctness.

## Validation layers

```text
Machine-readable schema
        ↓
S118 structural / local semantic validation
        ↓
S129 cross-layer semantic invariants
        ↓
Graph projection validation
```

## Core invariants

The following distinctions must not be collapsed:

- Measurement ≠ Metric
- Metric ≠ KPI
- KPI ≠ Target
- Target ≠ Actual
- Recommendation ≠ Decision
- Decision ≠ Action
- Observation ≠ Inference
- Forecast ≠ Actual
- Plan ≠ Actual
- Event ≠ State
- Location ≠ Node
- Lane ≠ Route
- Route ≠ Flow

## Primitive vs derived

Core operational concepts must not be classified as derived merely because an implementation can calculate a related metric.

Examples of derived concepts include:

- Inventory Turns
- Days of Supply
- Service Level
- Capacity Utilization
- Risk Score

The validator therefore checks that derived declarations are explicit and that primitive/core concepts are not accidentally marked derived.

## Graph compatibility

S129 is intentionally storage-neutral. Graph validation remains a projection concern, but the same canonical concept and relationship names must be resolvable by graph validation.

A graph projection must not silently repair a semantic violation by collapsing concepts into generic labels or relationships.

## Non-goals

S129 does not determine whether a KPI target is reasonable, whether a plan is optimal, or whether a causal claim is scientifically true. Those are domain/decision/causal reasoning concerns.
