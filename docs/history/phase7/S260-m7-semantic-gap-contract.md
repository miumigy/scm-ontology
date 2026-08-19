# S260 — M7 Semantic Gap Classification Contract

## Purpose

Define how enterprise representations that cannot be safely canonicalized are classified without expanding the Canonical Ontology by assumption.

## Boundary

```text
Enterprise Representation
        ↓
   Mapping Decision
        ↓
  Semantic Gap Result
        ↓
  Evidence / Provenance
```

A Semantic Gap is a classification of a canonicalization limitation. It is not evidence that the Canonical Ontology is incomplete, and it MUST NOT automatically trigger ontology extension.

## Required gap classes

- `ambiguous`: more than one existing canonical interpretation remains plausible.
- `unmappable`: no existing canonical semantic can be justified for the representation.
- `unsupported`: the adapter intentionally does not support the representation or transformation.
- `vendor_specific`: the representation expresses a vendor-specific concept with no justified canonical equivalent.
- `insufficient_evidence`: a plausible mapping exists, but available evidence is insufficient to assert the mapping safely.
- `conflicting_semantics`: source semantics conflict with the selected canonical interpretation or with other authoritative mappings.

These classes describe different causes and MUST NOT be collapsed into a generic `unknown` state when the cause is known.

## Classification record

A gap record SHOULD preserve:

- `gap_class`
- `source_system`
- `source_representation`
- `mapping_attempt_id`
- `candidate_canonical_terms`, when applicable
- `reason`
- `provenance`
- `mapping_confidence`, when a mapping was attempted

A gap classification MUST preserve the source lineage. Lack of canonicalization MUST NOT erase the enterprise representation or its provenance.

## No ontology expansion by default

A Semantic Gap MUST NOT cause automatic creation, modification, or extension of a canonical entity, attribute, predicate, or relationship.

In particular:

- `vendor_specific` does not become a new canonical concept automatically;
- `unmappable` does not become a new predicate automatically;
- `insufficient_evidence` does not become a Canonical Fact;
- `ambiguous` does not select a canonical interpretation by convenience.

Any future ontology change requires a separate, explicit ontology-governance decision with independent evidence.

## Canonicalization result states

A canonicalization pipeline MUST be able to return a non-canonicalized result while preserving the mapping attempt:

```text
mapped
ambiguous
unmappable
unsupported
vendor_specific
insufficient_evidence
conflicting_semantics
```

A Semantic Gap result is therefore an explicit outcome, not an exception to be hidden or silently repaired.

## Evidence and provenance boundary

Evidence may explain why a gap was classified, and provenance records where the representation originated. Neither one alone establishes a Canonical Fact.

`mapping_confidence` expresses confidence in the mapping decision, not confidence that an underlying business fact is true.

## Read-only invariant

Semantic Gap classification is read-only with respect to canonical ontology and canonical facts. The adapter:

- MUST NOT create a new canonical entity, attribute, or predicate automatically;
- MUST NOT mutate canonical facts;
- MUST NOT infer a canonical fact from a gap classification;
- MUST NOT conceal a gap by selecting an arbitrary canonical concept;
- MUST NOT use a vendor-specific representation as implicit authority for ontology extension.

## Governance handoff

A repeated or material Semantic Gap MAY become an input to future ontology governance, adapter backlog prioritization, or evidence collection. That workflow is explicitly outside canonicalization execution and MUST NOT mutate the Canonical Ontology as a side effect of processing source data.

## Non-goals

S260 does not define automatic ontology learning, ontology governance procedures, vendor connector implementation, or canonical graph mutation.
