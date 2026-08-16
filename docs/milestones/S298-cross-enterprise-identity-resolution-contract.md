# S298 — M8 Cross-enterprise Identity Resolution Contract

## Purpose

Define the governance boundary for determining whether identities from different enterprise boundaries may refer to the same Canonical Entity.

## Enterprise boundary

- Enterprise identity scope MUST remain explicit for every cross-enterprise identity assertion.
- Organization, legal-entity, tenant, or equivalent ownership scope MUST NOT be inferred solely from identifier similarity.
- An external identifier MUST retain its issuing enterprise and source context.
- Cross-enterprise identity linkage MUST be attributable to an explicit governed decision.

## Canonical identity safety

- A cross-enterprise match MUST NOT automatically create or mutate a Canonical Entity.
- Identity similarity, shared identifiers, or reciprocal source agreement MUST NOT by themselves establish Canonical Identity.
- A Canonical Identity MUST NOT be silently shared across enterprise boundaries.
- Enterprise-specific semantics MUST NOT be promoted into Canonical semantics solely because two enterprises agree.
- Cross-enterprise resolution MUST NOT be treated as an implicit Canonical mutation.

## Evidence, provenance, and authority

- Every cross-enterprise identity decision MUST preserve source identity, enterprise scope, provenance, evidence, and decision context.
- The authority and scope under which the linkage was established MUST remain observable.
- Evidence MUST remain distinguishable from the resulting identity decision.
- Missing, conflicting, expired, or insufficient authority MUST produce an observable unresolved or rejected outcome rather than an implicit match.

## Resolution outcomes

A cross-enterprise identity resolution MUST explicitly represent one of: `matched`, `not_matched`, `ambiguous`, `unresolved`, `conflict`, or `rejected`.

`ambiguous`, `unresolved`, `conflict`, and `rejected` MUST remain first-class outcomes and MUST NOT be coerced into `matched` for downstream convenience.

## History and replay

- Cross-enterprise Identity Decisions MUST be append-only.
- Historical cross-enterprise Identity Decisions MUST NOT be silently rewritten.
- A changed decision MUST be recorded as a new attributable decision linked to the prior decision.
- Resolution MUST be replayable from the recorded source identities, enterprise scopes, evidence, provenance, authority context, and decision inputs.

## Downstream application boundary

A cross-enterprise identity decision MAY be supplied to a later governed Application step only when that step explicitly evaluates its enterprise scope and authority. Identity resolution itself MUST NOT authorize Canonical mutation, data sharing, or unrestricted downstream propagation.

## Non-goals

This slice does not define legal/privacy policy, consent implementation, authorization infrastructure, probabilistic thresholds, ML model selection, automatic entity merging, graph transactions, vendor connectors, data-sharing enforcement, or autonomous Canonical mutation.
