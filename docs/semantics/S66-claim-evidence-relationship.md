# S66 — Claim–Evidence Relationship Semantics

## Purpose

S66 connects Claim and EvidenceReference through the existing first-class relationship concept rather than introducing a specialized evidence-link schema.

Canonical shape:

```text
Claim
  │
  │ predicate
  ▼
EvidenceReference
```

A concrete relationship has its own identity:

```text
ClaimEvidenceRelationship
├─ relationship_id
├─ claim_id
├─ predicate
└─ evidence_id
```

## Predicate semantics

`predicate` remains open vocabulary. `supported_by` is a natural canonical example, but S66 does not close the vocabulary to a fixed enum. This permits relationships such as `corroborated_by` or future domain-specific evidence semantics without changing the structural contract.

## Why this is a relationship

The relationship itself may later carry canonical relationship qualifiers and validity semantics established by earlier contracts. Therefore S66 does not create a parallel `EvidenceLink` abstraction.

Conceptually:

```text
Relationship
├─ identity
├─ endpoints
├─ predicate
├─ qualifiers
└─ validity
```

S66 only defines the Claim–Evidence endpoint semantics needed to connect the existing concepts.

## Boundary

```text
ClaimEvidenceRelationship
    ≠ Evidence
    ≠ Provenance
    ≠ Audit Log
    ≠ Data Lineage
    ≠ Confidence Score
```

S66 does not define evidence strength, confidence, truth evaluation, contradiction resolution, or source-system storage.
