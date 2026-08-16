# S301 — M8 Canonical Fact Application & Version Transition Contract

## Purpose

Define the governed application boundary that converts an approved Canonical Graph Write Intent into an explicit Canonical Fact Version and lifecycle transition, while preserving the invariants established by S299 and S300.

## Application preconditions

- A Fact Application MUST reference an explicit governed Write Intent.
- The Write Intent MUST identify the target Canonical Fact, requested operation, expected current version/state, governing decision, authorization, provenance, evidence, and idempotency context.
- Application MUST validate the expected current version/state before creating a new Fact Version or lifecycle transition.
- A stale, conflicting, unauthorized, or incomplete Write Intent MUST NOT produce a Canonical Fact mutation.

## Version creation

- A successful application MUST create a new attributable Fact Version when the governed operation changes Canonical Fact state.
- The new Fact Version MUST preserve lineage to the prior version when one exists.
- The prior version MUST remain historically retrievable.
- A version transition MUST NOT overwrite the prior version's historical content.
- The resulting lifecycle state MUST be explicit and valid under S300.

## Lifecycle transition

- Every lifecycle transition MUST identify its source version, resulting version/state, governing decision, application context, and recorded time.
- Supersession MUST explicitly reference the version it supersedes.
- Invalidation, retirement, dispute, and deferral MUST remain distinguishable from successful activation.
- A lifecycle transition MUST NOT silently convert an unresolved, conflicting, or rejected decision into an active Canonical Fact.

## Atomicity and observable outcomes

The application boundary MUST produce one attributable outcome for the governed operation: `applied`, `rejected`, `deferred`, `conflict`, `stale`, or `failed`.

- An `applied` outcome MUST reference the resulting Fact Version.
- A `rejected`, `deferred`, `conflict`, `stale`, or `failed` outcome MUST NOT be represented as an applied Canonical mutation.
- Partial execution MUST remain observable and MUST NOT be reported as successful application.
- Recovery or compensation MUST create an explicit governed record and MUST preserve the original application history.

## Idempotency

- Repeated application of the same accepted Write Intent MUST resolve to the same governed application outcome without creating unintended duplicate Fact Versions.
- Idempotency MUST be evaluated using the declared application identity/idempotency key and relevant target/version context.
- A replay against a changed current version MUST re-evaluate preconditions rather than bypassing them.

## Provenance and audit

- Every application outcome MUST retain the Write Intent, governing decision, authorization, source identity, enterprise scope, provenance, evidence, and application context references required by S299 and S300.
- Application History MUST be append-only.
- Historical application outcomes and Fact Versions MUST NOT be silently rewritten.
- Current Canonical Truth MUST remain reconstructable from the resulting Fact Version and its governed lineage.

## Boundary against implicit mutation

Identity Resolution, Conflict Resolution, Mapping, Reasoning, semantic similarity, evidence evaluation, or replay MUST NOT directly perform Fact Application. Only the explicit governed application step MAY create a new Canonical Fact Version or lifecycle transition.

## Non-goals

This slice does not define a storage transaction implementation, distributed consensus, authorization implementation, database locking, automatic conflict resolution, probabilistic identity matching, ontology learning, vendor connectors, or unrestricted ingestion. It defines the application and transition contract those implementations MUST satisfy.
