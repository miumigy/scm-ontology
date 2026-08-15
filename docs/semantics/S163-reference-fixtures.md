# S163 — Canonical Reference Fixtures

S163 introduces a small, stable SCM reference instance for regression and semantic review.

## Purpose

Fixtures are not production sample data and do not define a new ontology concept. They prove that the canonical model can represent a concrete SCM observation while preserving context.

```text
Inventory:001
  └─ quantity_on_hand = 100
       └─ Observation Context
```

The fixture is validated against the published S161 JSON Schema.

## Design rules

- Keep fixtures intentionally small and deterministic.
- Use canonical references, not vendor-specific field names.
- Preserve assertion context.
- Do not encode enterprise mapping assumptions.
- Fixtures are regression contracts, not normative business master data.
