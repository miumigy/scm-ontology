# S77 — Evidence Source Semantics

S77 defines the semantic boundary between an Evidence reference and the source from which that evidence originates.

## Canonical decision

`EvidenceReference.reference` identifies the Evidence object or evidence artifact represented by the Canonical EvidenceReference. It does not identify the source/provenance of that evidence.

```text
EvidenceReference
├─ evidence_id
├─ evidence_type
└─ reference          ← reference to the evidence

source/provenance    ← separate semantic concern
```

No required `source_reference` field is added to `EvidenceReference` in S77.

## Why source is separate

An evidence item may originate from an enterprise system, organization, document, person, observation process, or external source. Encoding these implementation-specific forms directly into Evidence would turn the Canonical Model into a data-lineage or persistence schema.

For example:

```text
Evidence
  evidence_id   = E1
  evidence_type = purchase_order
  reference     = PO-2026-001
```

`PO-2026-001` identifies the evidence reference. It does not, by itself, assert that SAP, a supplier, a document repository, or a particular organization is the source.

## Provenance boundary

Source/provenance may be represented by a future explicit semantic relationship when its semantics are sufficiently stable, for example:

```text
Evidence ──derived_from──→ Source
```

or through a separate Semantic Mapping / provenance layer.

S77 does not choose or require such a relationship yet.

## Distinctions

```text
Evidence reference
    ≠ evidence source
    ≠ source system
    ≠ database key
    ≠ document URI
    ≠ audit log
    ≠ data lineage record
```

A reference value may happen to be a URI, ERP identifier, document identifier, or other enterprise identifier, but the Canonical Model treats it as opaque as established by S70.

## Evidence type

`evidence_type` describes the semantic type/category of the evidence. It does not identify the source. The vocabulary remains open.

## Non-goals

S77 does not define a Source entity, source-system model, provenance graph, audit-log schema, data-lineage model, URI policy, identity-resolution algorithm, or persistence-specific foreign key.
