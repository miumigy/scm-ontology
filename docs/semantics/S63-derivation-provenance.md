# S63 — Derivation Provenance Integration

## Purpose

S63 connects the existing derivation model with provenance without replacing the existing `Provenance` contract.

S54 defines concrete inference application through `InferenceStep` and ordered `Derivation`. S62 defines the semantic `InferenceRule`. S63 adds the smallest bridge needed to describe why a concrete derivation step is supported by particular input facts and source relationships.

## Canonical bridge

```text
InferenceRule
     ↓ defines
InferenceStep
     ↓ applies to
Input Facts
     ↓ produces
Derived Fact
     ↓ explained by
DerivationProvenance
```

`DerivationProvenance` contains:

- `rule_id`
- `input_fact_ids`
- `source_relationship_ids`

`input_fact_ids` identifies the concrete semantic facts consumed by the derivation. `source_relationship_ids` optionally identifies relationships that provide supporting semantic context.

## Boundary

S63 does not redefine the existing `Provenance` type, `Derivation`, or `InferenceStep`.

It also does not introduce:

- audit logs
- event sourcing
- database lineage
- natural-language explanations
- evidence quality scoring
- provenance inference
- source storage

The contract records provenance references; it does not establish whether a source is trustworthy or how provenance is rendered.

## Important distinction

```text
Provenance
    ≠ Audit Log
    ≠ Event Sourcing
    ≠ Data Lineage
    ≠ Explanation
```

The canonical model should retain provenance as semantic references rather than implementation-specific history.
