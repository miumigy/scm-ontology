# S290 — Identity Resolution Decision Contract

## Purpose

Define the governed decision boundary that converts identity-resolution evidence into an auditable decision without allowing matching or confidence to mutate Canonical Identity implicitly.

## Decision Inputs

A resolution decision MUST reference the identity-resolution proposal and its evidence context.

The decision MUST preserve source identity, provenance, evidence references, uncertainty, and the identities considered.

The decision context MUST identify the governing policy or rule set used to reach the decision.

## Decision Outcomes

A decision MAY produce an explicit outcome such as:

- accepted for governed application
- rejected
- unresolved
- conflicting
- deferred for review

Unresolved and conflicting outcomes MUST remain first-class and MUST NOT be coerced into acceptance.

## Canonical Safety Invariants

- Identity similarity MUST NOT by itself establish Canonical Identity.
- Confidence MUST NOT by itself authorize Canonical Identity mutation.
- MUST NOT create a new canonical entity, attribute, or predicate automatically.
- MUST NOT mutate canonical facts implicitly.
- MUST NOT silently resolve ambiguous mappings or identities.
- Source identity and provenance MUST remain attached.
- Conflicts MUST remain observable.
- Reasoning MUST remain read-only.

## Governed Application

An accepted decision is an authorization boundary for a separately governed Application step; it is not itself an implicit graph mutation.

Canonical Identity mutation MUST require the explicit governed Application step and an auditable application record.

Any change to the decision basis MUST result in a new decision record rather than silently rewriting the historical decision.

## Audit and Replay

Identity-resolution decisions MUST be append-only and replayable from their recorded inputs and evidence references.

A replay MUST NOT rewrite the historical decision. Differences caused by changed evidence, mappings, semantics, or governance MUST remain observable as replay drift.

## Non-Goals

This contract does not define a matching algorithm, approval UI, authorization implementation, merge executor, production graph transaction, or automatic conflict resolution.
