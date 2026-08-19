# S280 — M8 Identity Evidence / Match Decision Contract

## Purpose

Define the evidence and decision boundary between a Candidate Identity Match and a Governed Canonical Identity.

S280 does not determine identity automatically. It defines what must be recorded before a governed identity decision can be applied.

## Decision model

```text
Source Identity
      ↓
Identity Evidence
      ↓
Candidate Identity Match
      ↓
Match Decision
      ↓
Governed Canonical Identity
```

A match score, similarity, or single evidence item is not sufficient by itself to establish Canonical Identity.

## Required decision record

A governed identity decision MUST preserve:

- source identities considered;
- candidate canonical identity, if any;
- evidence references and provenance;
- evidence interpretation;
- confidence or decision strength;
- ambiguity and unresolved conditions;
- conflict information;
- decision actor or governed process;
- decision timestamp/version;
- rationale sufficient for replay and explanation.

## Safety invariants

1. Identity evidence MUST remain distinguishable from Canonical Truth.
2. Evidence MUST NOT be promoted to Canonical Identity automatically.
3. A confidence score MUST NOT by itself establish Canonical Identity.
4. Ambiguous or insufficient evidence MUST remain an explicit unresolved outcome.
5. Conflicting evidence MUST remain observable and MUST NOT be silently discarded.
6. Provenance MUST remain attached to the evidence and decision record.
7. A governed decision MUST be auditable and replayable.
8. Reasoning MUST remain read-only.
9. The decision process MUST NOT create a new canonical entity, attribute, or predicate automatically.
10. The decision process MUST NOT mutate canonical facts without an explicit governed application step.

## Semantic boundary

The following distinctions are mandatory:

- **Evidence**: an observed or supplied basis for considering an identity correspondence.
- **Candidate Identity Match**: a proposed correspondence that remains subject to governance.
- **Match Decision**: an explicit governed decision concerning the candidate.
- **Governed Canonical Identity**: an approved identity correspondence that may be consumed by a separately governed graph application step.

## Non-goals

S280 does not implement probabilistic entity-resolution algorithms, automatic threshold-based identity approval, vendor-specific matching logic, master-data workflows, or autonomous graph mutation.
