# S70 — Evidence Reference Semantics

## Purpose

S70 defines the minimum canonical meaning of `EvidenceReference.reference`.

An `EvidenceReference` identifies or points to a source that can support a semantic claim. The reference value is intentionally opaque to the canonical model.

```text
EvidenceReference
├─ evidence_id
├─ evidence_type
└─ reference
```

## Reference semantics

`reference` may identify either:

- a canonical ontology object, such as an Observation identifier (`O1`); or
- an external or implementation-specific source, such as an ERP record reference or document URI.

The canonical model does **not** prescribe the representation of the reference.

Therefore:

```text
reference
≠ database key
≠ UUID
≠ URI
≠ URL
≠ persistence identifier
```

A URI-like value is allowed, but URI parsing or validation is outside this contract.

## Evidence type semantics

`evidence_type` remains an open vocabulary. The canonical model does not enumerate all possible evidence source types.

Examples include:

```text
observation
erp_record
document
custom_enterprise_source
```

These are semantic labels, not a closed enum.

## Resolution boundary

Resolving a reference to an actual object is a separate concern from representing the reference.

```text
EvidenceReference
       │
       │ opaque reference
       ▼
Reference Resolution
       │
       ▼
Canonical / External Source
```

Reference resolution may later be implemented by SCM Graph infrastructure, a semantic mapping layer, or an application. It is not part of the Canonical Semantic Model.

## Relationship to S69

S69 established that an Observation can be used as an evidence source through:

```text
EvidenceReference(
    evidence_type="observation",
    reference=<observation_id>
)
```

S70 generalizes this principle without creating an Observation-specific reference primitive.

## Explicit non-goals

S70 does not define:

- URI syntax or validation
- UUID generation
- database identifiers
- source-system connectors
- reference resolution algorithms
- dereferencing behavior
- evidence trust or quality
- evidence provenance
- access control
