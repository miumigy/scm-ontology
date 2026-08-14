# S64 — Canonical Evidence Reference

## Purpose

S64 defines the smallest canonical primitive for referencing evidence that supports a semantic claim.

```text
Claim / Fact
    │
    └─ supported_by → EvidenceReference
```

## Canonical structure

`EvidenceReference` contains:

- `evidence_id` — identity of the evidence reference
- `evidence_type` — semantic category of the evidence
- `reference` — identifier or locator for the referenced evidence

The model does not prescribe whether the reference points to an ERP record, document, sensor observation, external source, or human assertion.

## Boundary

EvidenceReference is a semantic reference, not the evidence payload itself.

It does not define:

- source-system schemas
- document storage
- URLs or URI schemes
- authentication
- evidence quality
- confidence or trust scores
- audit logging
- event sourcing
- data lineage storage
- natural-language explanation generation

## Evidence vs provenance

```text
Evidence
  = what can support a claim

Provenance
  = how a claim was derived / where its derivation came from
```

A derived fact can therefore have both:

```text
DerivedFact
├─ provenance → inference rule + inputs
└─ evidence   → supporting source references
```

The two concepts must not be collapsed.

## Open-world principle

`evidence_type` is intentionally a vocabulary value rather than a closed enum. Domain-specific evidence types may be introduced without changing the canonical primitive.
