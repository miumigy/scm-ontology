# S267 — M7 Governance Decision Contract

## Purpose

Define the controlled boundary between a reviewable governance signal and a human-approved mapping or ontology decision.

## Decision boundary

```text
Governance Signal
      ↓
Controlled Review
      ↓
★ Governance Decision
      ↓
Approved Mapping / Proposal
```

A Governance Decision is an explicit controlled decision. It is not created merely by observing a replay difference or by receiving a governance signal.

## Decision identity

A decision MUST preserve:

- `decision_id`
- `signal_id`
- `decision_state`
- `decision_reason`
- `decided_by`
- `decided_at`
- `mapping_rule_version`
- `adapter_version`
- `scope`

The decision MUST remain traceable to the signal and evidence that motivated the review.

## Decision states

A controlled review MAY produce:

- `approved`
- `rejected`
- `deferred`
- `needs_more_evidence`

A decision state MUST be explicit. Absence of a decision MUST NOT be interpreted as approval.

## Approval boundary

An `approved` decision authorizes the specific action described by its scope. It MUST NOT silently authorize unrelated ontology expansion, mapping changes, or Canonical Fact mutation.

A proposal for a new canonical concept remains a proposal until accepted through the applicable ontology-governance process.

## Canonical Truth boundary

Governance Decisions:

- MUST NOT create a new canonical entity, attribute, or predicate automatically;
- MUST NOT mutate canonical facts as a side effect of review;
- MUST NOT infer a canonical fact from approval alone;
- MUST NOT rewrite historical audit records;
- MUST preserve the distinction between an approved mapping and an asserted business fact.

## Evidence and provenance

Approval MUST NOT erase ambiguity, provenance, semantic gaps, or contradictory evidence. Relevant evidence references SHOULD remain attached to the decision.

An approval may establish that a mapping rule is accepted for a defined scope. It does not establish that every enterprise record processed by that rule is true.

## Versioning

A governance decision MUST identify the mapping-rule and adapter versions to which it applies. A later version requires a new controlled decision when its semantics materially differ.

## Explainability

A reviewer MUST be able to determine what was decided, why it was decided, by whom, when, and within what scope.

## Non-goals

S267 does not implement workflow software, automatic approval, Canonical Fact ingestion, automatic ontology learning, vendor connectors, or graph mutation.
