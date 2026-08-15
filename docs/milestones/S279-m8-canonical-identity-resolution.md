# S279 — M8 Canonical Identity Resolution Contract

## Purpose

Define the semantic and governance boundary for resolving whether distinct enterprise source identities refer to the same Canonical Entity.

S279 operates after M7 Canonicalization and within the M8 shared-graph integration boundary. Identity resolution is a governed decision process, not an ontology-learning mechanism.

## Identity states

A resolution workflow MUST distinguish:

- **Source Identity** — an identity asserted by an enterprise system;
- **Candidate Identity Match** — a proposed correspondence between source identities;
- **Governed Canonical Identity** — an explicitly approved correspondence to a Canonical Entity.

A Candidate Identity Match MUST NOT be treated as a Governed Canonical Identity without an explicit governed application step.

## Required invariants

1. Identity similarity MUST NOT by itself establish Canonical Identity.
2. The resolver MUST preserve source identity and provenance for every candidate and decision.
3. The resolver MUST preserve the evidence and rationale supporting a governed decision.
4. Ambiguous identity matches MUST remain observable and MUST NOT be silently resolved.
5. Unresolved identity MUST remain a first-class outcome.
6. Conflicting evidence MUST remain observable and MUST NOT be silently discarded.
7. A failed or low-confidence match MUST NOT create a new canonical entity automatically.
8. Identity resolution MUST NOT create a new canonical entity, attribute, or predicate automatically.
9. Identity resolution MUST NOT mutate canonical facts implicitly.
10. Reasoning MUST remain read-only; a reasoning result MUST NOT itself authorize graph mutation.
11. Resolution decisions MUST be replayable from recorded inputs, evidence, and governed decisions.
12. Historical resolution decisions MUST remain auditable and MUST NOT be silently rewritten.

## Confidence boundary

Confidence is metadata about a resolution decision, not Canonical Truth.

A high similarity score, deterministic key match, or model prediction MAY support a Candidate Identity Match, but MUST NOT alone establish a Governed Canonical Identity unless the applicable governance policy explicitly permits that decision and records the governing rule.

## Semantic Gap boundary

When the available enterprise representations do not contain enough evidence to establish identity, the result MUST be classified explicitly, for example as:

- unresolved identity;
- ambiguous identity;
- conflicting identity evidence; or
- insufficient evidence.

The resolver MUST NOT expand the Canonical Ontology merely because identity resolution is unsuccessful.

## Non-goals

S279 does not define probabilistic model selection, vendor-specific matching algorithms, production master-data governance workflows, automatic ontology learning, or autonomous graph mutation.

Those mechanisms may be introduced later only through explicit contracts that preserve the M7/M8 semantic boundary.

## Acceptance criterion

S279 is conformant when an identity-resolution process can distinguish source identity, candidate match, and governed canonical identity while preserving provenance, evidence, ambiguity, confidence, auditability, and unresolved outcomes without implicitly changing Canonical Semantics.
