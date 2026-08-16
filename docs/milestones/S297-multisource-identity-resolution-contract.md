# S297 — M8 Multi-source Identity Resolution Contract

## Purpose

Define a governed boundary for resolving whether source identities refer to the same Canonical Entity across multiple enterprise sources.

## Identity model

- Source Identity and Canonical Identity MUST remain distinct concepts.
- A Source Identity MUST retain source-system identity, source scope, and provenance.
- A Canonical Identity MUST NOT be created automatically from a successful match.
- A mapping between Source Identity and Canonical Identity MUST be attributable to an explicit decision.
- One Canonical Entity MAY have multiple source identities, but their lineage MUST remain observable.

## Resolution outcomes

An identity resolution result MUST explicitly represent one of: `matched`, `not_matched`, `ambiguous`, `unresolved`, or `conflict`.

`ambiguous`, `unresolved`, and `conflict` MUST remain first-class outcomes and MUST NOT be coerced into a match merely to complete processing.

## Evidence and provenance

- Every identity decision MUST preserve its source identity, provenance, evidence, and decision context.
- Identity similarity, deterministic key equality, or mapping success MUST NOT by itself establish Canonical Identity.
- Conflicting identifiers or evidence MUST remain observable.
- Provenance MUST remain attached to the identity decision and MUST NOT be silently discarded.

## Canonical safety boundary

- The resolution process MUST NOT create a new canonical entity, attribute, or predicate automatically.
- The resolution process MUST NOT mutate Canonical facts implicitly.
- Identity resolution MUST NOT be treated as an implicit Canonical mutation.
- A resolved identity MAY be supplied to a later governed Application step, but that step MUST be explicit and separately authorized.
- Semantic Gap and unresolved identity MUST remain observable outcomes.

## Decision history

- Identity Decisions MUST be append-only.
- Historical Identity Decisions MUST NOT be silently rewritten.
- A changed decision MUST be represented as a new attributable decision linked to the prior decision.
- Identity resolution MUST be replayable from recorded inputs, evidence, provenance, and decision context.

## Cross-source constraints

Source-specific semantics MUST NOT be promoted into Canonical semantics solely because multiple sources agree. Agreement across sources is evidence for a decision, not automatic proof of Canonical Identity.

## Non-goals

This slice does not define probabilistic thresholds, ML model selection, automatic entity merging, graph transactions, authorization implementation, distributed locking, vendor connectors, or autonomous Canonical mutation.
