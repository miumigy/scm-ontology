# S65 — Canonical Claim / Assertion

## Purpose

S65 defines a minimal semantic object for a statement that can be supported, contradicted, observed, or derived without making the statement itself an observation, fact, rule, or evidence payload.

## Canonical structure

```text
Claim
├─ claim_id
├─ subject_id
├─ predicate
└─ object_value
```

A Claim represents a semantic assertion such as:

```text
Shipment-001 ──has_status──→ delivered
```

The object may be an entity identifier or a literal value. S65 does not prescribe a database representation or RDF serialization.

## Why Claim is separate from Fact

A claim is a statement that may be asserted or supported. A fact is a semantic state of knowledge used by the ontology's observation/derivation model.

```text
Claim
  = statement being asserted

Fact
  = semantic information represented as known/observed/derived
```

S65 deliberately does not define truth status, confidence, belief, or epistemic scoring.

## Evidence boundary

Evidence supports a claim; it is not embedded in the Claim primitive.

```text
Claim
   │
   └─ supported_by → EvidenceReference
```

The relationship between Claim and Evidence can therefore be represented without making evidence storage part of the canonical Claim object.

## Inference boundary

A Claim is not an inference rule or inference result.

```text
Claim
  ≠ Fact
  ≠ Evidence
  ≠ Provenance
  ≠ InferenceRule
  ≠ Constraint
  ≠ Policy
```

An inference runtime may use claims as premises or conclusions, but S65 does not prescribe that execution behavior.

## Open-world principle

`predicate` is intentionally an open vocabulary value. Domain-specific predicates are not rejected merely because they are not present in a core vocabulary.

## Deliberate omissions

S65 does not define:

- truth or falsity semantics
- confidence or trust scores
- assertion author
- source-system identity
- evidence collections
- contradiction resolution
- temporal validity
- RDF/OWL serialization
- query or evaluation behavior
