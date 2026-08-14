# S72 — Claim Subject Semantics

## Semantic Contract

A Claim subject identifies the entity or resource about which the claim is made.

The existing `Claim.subject_id` field is the canonical subject reference. It is an opaque, non-empty reference value. S72 does not introduce a separate `ClaimSubject` primitive.

```text
Claim
├─ subject_id      -> opaque reference
├─ predicate       -> open predicate vocabulary
└─ object_value    -> claim object
```

The subject reference may identify a canonical SCM entity or an external/domain-specific resource. Reference resolution is outside this contract.

## Reuse of Reference Semantics

S72 reuses the opaque reference semantics established by S70. The subject is inherently reference-like; unlike a Claim object, it has no literal-value form in this contract.

Therefore the canonical model does not need a redundant `ClaimSubject` wrapper.

## Boundaries

`subject_id` is:

- a semantic reference, not a database foreign key
- not required to be a URI, URL, UUID, or other identifier format
- not a literal claim value
- not a persistence or identity-resolution contract

Examples:

```text
subject_id = "Shipment-001"
subject_id = "erp://shipment/001"
subject_id = "enterprise-specific-subject"
```

All are valid opaque references. The canonical model does not parse or dereference them.

## Backward Compatibility

The existing `Claim.subject_id: str` field remains unchanged. S72 clarifies its canonical semantics rather than replacing it with a new type or changing the existing Claim constructor.

## Explicitly Out of Scope

S72 does not define:

- URI/IRI syntax
- UUID generation
- database foreign keys
- identity resolution
- entity existence checks
- subject type constraints
- persistence semantics
- graph serialization
