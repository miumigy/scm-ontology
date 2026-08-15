# S271 — M7 Semantic Gap Review Contract

## Purpose

Define the controlled review boundary for Semantic Gaps discovered during enterprise canonicalization, reconciliation, or effectiveness assessment.

## Review boundary

```text
Semantic Gap
      ↓
Gap Classification
      ↓
Controlled Review
      ↓
★ Resolution Decision
      ↓
Mapping / Evidence / Ontology Governance
```

A Semantic Gap is an explicit representation of insufficient, ambiguous, or incompatible semantics. It MUST NOT be treated as permission to invent a Canonical concept.

## Gap classification

A gap MAY be classified as:

- `ambiguous_mapping`
- `unmappable_representation`
- `missing_evidence`
- `conflicting_evidence`
- `unsupported_scope`
- `canonical_coverage_gap`

The classification MUST describe the observed semantic problem, not prescribe an invented Canonical answer.

## Review record

A review SHOULD preserve:

- `gap_id`
- source representation reference
- adapter and mapping versions
- gap classification
- evidence references
- affected scope
- review status
- resolution decision reference
- reviewed_at

The review MUST remain traceable to the enterprise representation and evidence that exposed the gap.

## Resolution options

A controlled review MAY resolve a gap by:

- accepting an existing mapping;
- requesting additional evidence;
- defining a scoped mapping rule;
- rejecting the enterprise representation for the declared scope;
- proposing a Canonical Ontology change through separate ontology governance.

A proposal for ontology change remains a proposal until separately approved.

## Canonical Truth boundary

Semantic Gap review:

- MUST NOT create a new canonical entity, attribute, or predicate automatically;
- MUST NOT mutate canonical facts;
- MUST NOT infer a canonical fact from absence of a gap alone;
- MUST NOT rewrite historical audit records;
- MUST NOT treat successful mapping as proof of the underlying business fact;
- MUST NOT silently expand an approved mapping beyond its declared scope.

## Evidence boundary

Closing a Semantic Gap requires an explicit reason and SHOULD retain the evidence supporting closure. Lack of a recorded gap does not mean evidence exists; absence of evidence MUST remain distinguishable from evidence of absence.

## Change control

A resolution that changes mapping behavior MUST proceed through a versioned controlled decision. A resolution that proposes Canonical Ontology change MUST use the applicable ontology-governance process.

Existing historical results remain associated with the versions under which they were produced.

## Explainability

A reviewer SHOULD be able to determine what semantic gap was observed, what evidence was considered, what resolution was selected, who decided it, and which future scope or version is affected.

## Non-goals

S271 does not define automatic ontology expansion, automatic rule generation, Canonical Fact ingestion, vendor connectors, workflow software, or graph mutation.
