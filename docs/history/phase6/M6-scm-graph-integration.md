# M6 — SCM Graph Integration

## Purpose

M6 moves SCM Ontology from validated semantic/reasoning contracts into executable canonical SCM Graph fixtures and end-to-end business-question validation.

## Scope

M6 validates the operational chain:

```text
Enterprise-like Data
        ↓
Adapter Mapping
        ↓
Canonical SCM Graph
        ↓
Query / Constraints
        ↓
Reasoning Runtime
        ↓
Evidence / Explanation / Confidence
        ↓
Business Answer
```

## Acceptance criteria

1. At least three executable canonical SCM Graph fixtures exist.
2. Fixtures cover material/product, site, inventory, capacity, lead-time, and supply-risk relationships across the validated M5 patterns.
3. At least three end-to-end business questions execute against canonical graph fixtures.
4. At least one fixture demonstrates enterprise-to-canonical mapping with provenance.
5. Reasoning remains read-only by default and does not silently promote inferred facts.
6. Regression tests validate graph construction, query results, evidence, explanations, and confidence metadata.
7. Semantic gaps discovered during execution are classified before any ontology change.

## Non-goals

M6 does not yet deliver production ERP/WMS/TMS integration, autonomous agents, optimization, or autonomous graph mutation.

## Exit condition

M6 exits when the project demonstrates a reproducible executable path from SCM business question through canonical graph representation and reasoning to an explainable answer.
