# S76 — Evidence Role Semantics

S76 defines the semantic role of the predicate on `ClaimEvidenceRelationship`.

## Canonical decision

The evidence-role predicate is a canonical predicate with an epistemic/evidential role. It reuses the same open predicate mechanism established for canonical predicates, but its role is determined by the semantic context of a Claim–Evidence association.

```text
Canonical Predicate
├─ domain predicate
│   └─ e.g. supplies, contains, located_at
└─ evidential predicate
    └─ e.g. supports, contradicts, corroborates, qualifies
```

This is a semantic classification, not a new required `PredicateCategory` field or closed enumeration.

## Evidence roles

Representative evidential predicates include:

- `supports` — evidence provides support for the claim.
- `contradicts` — evidence provides information inconsistent with the claim.
- `corroborates` — evidence independently reinforces the claim.
- `qualifies` — evidence adds a qualification or contextual condition to the claim.

These are examples, not an exhaustive vocabulary. Domain- or enterprise-specific predicates remain permitted.

## Context matters

The predicate alone does not establish that an arbitrary edge is an evidence relationship. The semantic context is supplied by `ClaimEvidenceRelationship` and its endpoints:

```text
Claim ──[evidential predicate]──> Evidence
```

Thus `supports` is not a generic truth operator and `contradicts` does not perform automatic truth resolution.

## Distinctions

```text
Evidence role
    ≠ evidence truth
    ≠ claim truth
    ≠ source reliability
    ≠ confidence/probability
    ≠ relationship qualifier
```

The role belongs to the Claim–Evidence association itself, so it remains a predicate on `ClaimEvidenceRelationship` rather than an attribute of the Evidence entity.

## Open-world validation

Known evidential predicates may receive future semantic validation. Unknown predicates remain valid unless another contract explicitly constrains them.

This supports progressive validation without turning the ontology into a closed-world vocabulary.

## Non-goals

S76 does not define a `PredicateCategory` primitive, confidence scores, source reliability models, truth-resolution algorithms, contradiction resolution, automatic inference, or a closed evidential predicate enum.
