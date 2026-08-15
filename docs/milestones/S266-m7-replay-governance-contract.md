# S266 — M7 Replay Governance Signal Contract

## Purpose

Define how replay differences become reviewable governance signals without allowing replay machinery to mutate Canonical Truth.

## Signal boundary

```text
Historical Result
      ↓
Replay Result
      ↓
Difference Classification
      ↓
★ Governance Signal
      ↓
Human / Controlled Review
```

A Governance Signal identifies something that may require review. It is not a Canonical Fact and does not authorize mutation by itself.

## Signal content

A Governance Signal SHOULD preserve:

- `signal_id`
- `result_id`
- difference classification
- historical version context
- replay version context
- reason
- affected mapping dimensions
- provenance references
- semantic-gap references
- recorded time

The signal MUST remain traceable to the replay comparison that produced it.

## Trigger conditions

Signals MAY be raised for:

- changed canonical target;
- changed decision;
- changed mapping confidence;
- changed provenance;
- changed semantic-gap classification;
- non-reproducible execution;
- repeated ambiguity or unmappable outcomes.

`same_decision` does not require a governance signal merely because a replay occurred.

## Review boundary

A Governance Signal MAY initiate human review, adapter review, mapping-rule review, evidence review, or ontology-governance consideration.

The review workflow MUST be distinct from replay execution. A reviewer may approve, reject, or request a new mapping rule, but such a decision is a separate controlled action.

## Canonical Truth boundary

A Governance Signal:

- MUST NOT create a new canonical entity, attribute, or predicate automatically;
- MUST NOT mutate canonical facts;
- MUST NOT infer a canonical fact from a governance signal alone;
- MUST NOT rewrite historical audit records;
- MUST NOT expand the Canonical Ontology merely because an enterprise representation is unmappable;
- MUST NOT treat reviewer recommendation as an already-established Canonical Fact.

## Semantic Gap handling

An unmappable or ambiguous replay MAY produce a governance signal classified as a Semantic Gap. The signal MUST identify the gap rather than inventing a canonical target.

A proposed ontology extension remains a governance proposal until separately accepted under ontology governance controls.

## Explainability

Every governance signal MUST expose why it was raised and retain references sufficient to navigate back to the historical result, replay result, and relevant mapping versions.

## Non-goals

S266 does not define human workflow software, ontology governance implementation, automatic ontology learning, canonical fact ingestion, vendor connectors, or graph mutation.
