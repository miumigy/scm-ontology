# S69 — Observation–Evidence Semantics

## Decision

S69 intentionally introduces **no new production primitive**.

An `Observation` can already be represented as an evidence source by using the existing `EvidenceReference` contract:

```text
Observation
    observation_id = O1
    observed_at = 2026-08-01T10:30
    subject_id = Shipment-001

EvidenceReference
    evidence_id = E1
    evidence_type = observation
    reference = O1
```

This is sufficient to connect an observation to a claim through the existing claim/evidence semantics without creating an `ObservationEvidenceLink` type.

## Semantic roles

```text
Observation
  = what was observed, and when

EvidenceReference
  = a canonical reference to something that supports a claim

Claim
  = a semantic assertion
```

Therefore:

```text
Observation ≠ EvidenceReference ≠ Claim
```

## Why no new relationship?

`EvidenceReference.evidence_type` is intentionally open. An evidence reference may point to an observation, document, ERP record, human assertion, or other domain-specific source. Introducing a dedicated Observation→Evidence predicate would unnecessarily specialize Evidence around one source type.

The canonical composition is therefore:

```text
Observation
    ↓ referenced by
EvidenceReference
    ↓ supports
Claim
```

The existing reference field remains implementation-neutral: it does not prescribe a database key, URI scheme, document identifier format, or persistence mechanism.

## Boundary

S69 does not define:

- observation-to-claim truth semantics
- evidence strength
- confidence
- source reliability
- observation/event equivalence
- sensor models
- evidence storage
- provenance rules
- temporal inference

In particular:

```text
Observation time
    ≠ Evidence time
    ≠ Claim validity
    ≠ Event time
```

S69 is therefore a **composition contract**, not a new ontology primitive.
