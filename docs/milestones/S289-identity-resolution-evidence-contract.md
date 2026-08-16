# S289 — Identity Resolution Evidence Contract

## Purpose

Define the evidence boundary used to support enterprise identity-resolution proposals without allowing evidence to become Canonical Identity implicitly.

## Evidence Requirements

Every identity-resolution proposal MUST retain:

- source identity and source system
- evidence references
- matching rationale or signal description
- confidence or uncertainty representation
- provenance
- resolution status

Evidence MUST remain attributable to its originating source and observation context.

## Canonical Safety Invariants

- Evidence MUST NOT by itself establish Canonical Identity.
- MUST NOT create a new canonical entity, attribute, or predicate automatically.
- MUST NOT mutate canonical facts implicitly.
- MUST NOT infer Canonical Truth from confidence alone.
- Conflicts MUST remain observable.
- Ambiguous and unresolved identity MUST remain first-class outcomes.
- Reasoning MUST remain read-only.
- Vendor-specific matching semantics MUST NOT be imported into the Canonical Ontology implicitly.

## Evidence Change and History

New or changed evidence MUST produce an observable evidence revision rather than silently rewriting historical evidence.

Historical identity-resolution evidence MUST remain append-only.

A later resolution MAY reference earlier evidence, but MUST NOT erase the provenance or decision context of the earlier record.

## Governed Application Boundary

Evidence supports a proposed resolution. It does not authorize Canonical Identity mutation.

Canonical Identity application MUST require an explicit governed Decision and Application step with an auditable record.

## Non-Goals

This contract does not define scoring algorithms, thresholds, machine-learning models, entity merge execution, automatic conflict resolution, source synchronization, or production graph mutation.
