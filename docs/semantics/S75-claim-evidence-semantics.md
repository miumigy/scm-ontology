# S75 — Claim–Evidence Semantics

S75 defines the minimal canonical relation between a Claim and an EvidenceReference.

## Canonical form

```text
Claim
  │
  └─ ClaimEvidenceRelationship
        ├─ relationship_id
        ├─ claim_id
        ├─ predicate
        └─ evidence_id
```

The relation is first-class because the semantic role of evidence belongs to the Claim–Evidence association, not to the Claim alone or the Evidence source alone.

## Predicate semantics

The predicate uses the same open canonical predicate semantics established by S41 and S73. Typical evidence roles may include:

- `supports`
- `contradicts`
- `corroborates`
- `qualifies`

These examples are not a closed enumeration. Domain-specific predicates remain permitted.

## Meaning

`supports` means that the referenced evidence is considered supporting evidence for the claim. It does **not** mean that the evidence is itself asserted to be true, nor does it establish that the claim is true.

Likewise, `contradicts` describes the semantic role of evidence relative to a claim; it does not automatically resolve which statement is correct.

## Why a first-class relation

A simple `Claim → Evidence` field would lose the role of the evidence. The relation must carry the predicate because the same evidence may:

```text
E1 ──supports──────→ C1
E1 ──contradicts───→ C2
```

The evidence identity remains independent from the relation identity.

```text
relationship_id ≠ evidence_id ≠ claim_id
```

## Boundaries

```text
ClaimEvidenceRelationship
    ≠ Claim
    ≠ EvidenceReference
    ≠ Evidence truth
    ≠ Claim truth
```

The relation does not define confidence scores, probabilities, source reliability, epistemic truth, ranking, or automated truth resolution. Those concerns require separate contracts if needed.

## Non-goals

S75 does not define an evidence scoring model, Bayesian inference, confidence thresholds, source trust model, automatic contradiction resolution, graph persistence, or a closed predicate enumeration.
