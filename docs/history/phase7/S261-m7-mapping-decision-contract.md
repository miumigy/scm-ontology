# S261 — M7 Mapping Decision Contract

## Purpose

Define the explicit decision produced by enterprise canonicalization, while keeping the decision separate from Canonical Truth and from the source representation itself.

## Decision boundary

```text
Enterprise Representation
        ↓
 Entity / Attribute / Predicate Mapping
        ↓
 Provenance + Semantic Gap Analysis
        ↓
   Mapping Decision
        ↓
 Canonicalization Result
```

A Mapping Decision records what the adapter decided about semantic correspondence. It does not, by itself, assert that the underlying business fact is true.

## Decision states

A mapping decision MUST use an explicit state:

- `mapped`: an existing canonical semantic has sufficient justification.
- `ambiguous`: multiple canonical interpretations remain plausible.
- `unmappable`: no existing canonical semantic can be justified.
- `unsupported`: the adapter does not support the representation or transformation.
- `vendor_specific`: the representation has vendor-specific semantics without a justified canonical equivalent.
- `insufficient_evidence`: a plausible mapping exists but evidence is insufficient for a safe decision.
- `conflicting_semantics`: available semantics conflict and cannot be safely resolved.
- `rejected`: the mapping is intentionally excluded by contract or policy.

The state MUST NOT be inferred solely from a confidence score.

## Decision record

A Mapping Decision SHOULD preserve:

- `decision_id`
- `source_system`
- `source_representation`
- `mapping_target`, when applicable
- `decision_state`
- `mapping_confidence`, when applicable
- `reason`
- `provenance`
- `semantic_gap`, when applicable
- `adapter_version`
- `mapping_rule_id`

## Mapping confidence boundary

`mapping_confidence` measures confidence in the semantic correspondence decision. It MUST NOT be interpreted as:

- confidence that an underlying business fact is true;
- confidence that a source is authoritative;
- confidence that a mapped relationship is current;
- permission to create a Canonical Fact.

A high-confidence mapping can still result in a non-canonicalized artifact when the source representation is evidence only or when the canonical fact requires independent assertion.

## Decision ≠ Canonical Fact

A Mapping Decision is metadata about canonicalization. It MUST NOT be treated as a Canonical Fact merely because its state is `mapped`.

In particular:

- a mapped ERP field does not automatically become a Canonical Attribute Fact;
- a mapped enterprise relation does not automatically become a Canonical Relationship Fact;
- a mapped entity identifier does not automatically create a Canonical Entity;
- provenance does not establish truth.

Canonical Fact creation, when permitted by a separate ingestion contract, is outside S261.

## Determinism and explainability

Given the same source representation, adapter version, mapping rule version, and relevant provenance context, the Mapping Decision SHOULD be deterministic.

Every non-trivial decision MUST have an explainable `reason`. Ambiguous, rejected, and failed decisions MUST NOT be hidden behind a null result.

## Read-only invariant

Mapping Decision evaluation is read-only with respect to the Canonical Ontology and Canonical Facts. The adapter:

- MUST NOT create a new canonical entity, attribute, or predicate automatically;
- MUST NOT mutate canonical facts;
- MUST NOT infer a canonical fact from a mapping decision alone;
- MUST NOT treat `mapped` as equivalent to `true`;
- MUST NOT conceal semantic gaps by selecting an arbitrary target.

## Provenance and semantic-gap integration

S261 consumes the provenance and Semantic Gap results defined by S259 and S260. It MUST preserve both in the decision record rather than replacing them with a single confidence value.

## Non-goals

S261 does not define canonical fact ingestion, ontology governance, automatic ontology learning, vendor connector implementation, or graph mutation.
