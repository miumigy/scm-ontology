# S78 — Evidence Type Semantics

S78 defines the meaning of `EvidenceReference.evidence_type` without turning it into an implementation-specific schema or a closed entity-type registry.

## Canonical decision

`evidence_type` is an open semantic classification of the Evidence item itself.

```text
EvidenceReference
├─ evidence_id
├─ evidence_type   ← classification of the Evidence
└─ reference       ← opaque reference to the Evidence
```

It is not, by itself, the type of the entity or artifact identified by `reference`.

For example:

```text
evidence_type = "purchase_order"
reference     = "PO-2026-001"
```

means that the Evidence is classified as a purchase-order-type evidence item. It does not assert a separate canonical `PurchaseOrder` entity type, nor does it require `PO-2026-001` to be resolved as one.

## Distinctions

```text
evidence_type
    ≠ referenced entity type
    ≠ source type
    ≠ source system
    ≠ persistence type
```

An Evidence item may refer to a document, transaction, observation, snapshot, system record, or other artifact. The referenced artifact's own ontology semantics, if any, are resolved separately.

## Open vocabulary

Evidence types remain open vocabulary values. Representative values include:

- `purchase_order`
- `shipment_record`
- `inventory_snapshot`
- `observation`
- `document`
- `system_record`
- `transaction`

These examples are not an exhaustive enum. Enterprise-specific evidence types remain valid unless another contract explicitly constrains them.

This preserves progressive validation: a known evidence type may receive richer semantics later without rejecting unknown types today.

## Relationship to EvidenceReference

`evidence_id` identifies the canonical EvidenceReference instance.

`evidence_type` classifies that Evidence instance.

`reference` identifies the evidence/artifact reference and remains opaque under S70.

No dereferencing, entity-type inference, URI parsing, or identity resolution is implied by `evidence_type`.

## Relationship to Observation

`observation` may be used as an evidence type when the Evidence item represents an observation, but this does not make `Observation` and `EvidenceReference` the same primitive. S69's Observation–Evidence relationship remains the explicit semantic bridge.

## Non-goals

S78 does not define a closed evidence-type enum, an Entity Type hierarchy, a Source Type hierarchy, automatic type inference, URI interpretation, identity resolution, or a persistence-specific schema.
