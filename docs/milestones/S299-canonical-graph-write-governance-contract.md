# S299 — M8 Canonical Graph Write Governance Contract

## Purpose

Define the governed boundary for applying an approved change to the Canonical Graph without allowing identity resolution, conflict resolution, or other upstream reasoning to mutate Canonical Truth implicitly.

## Write intent

Every Canonical Graph write MUST be represented by an explicit Write Intent containing, at minimum:

- target Canonical Entity / Fact / relationship identity
- requested operation
- expected current version or state
- intended resulting state
- governing Decision / Resolution reference
- authorization and scope
- provenance and evidence references
- idempotency key
- audit context

A Write Intent MUST be attributable to the governed application step that produced it.

## Authorization and scope

- A Graph Write MUST require an explicit governed authorization appropriate to its scope.
- Identity Resolution, Conflict Resolution, Mapping, Reasoning, or Provenance processing MUST NOT itself authorize a Graph Write.
- A Write MUST be rejected when its authorization, scope, decision reference, or required evidence is missing or invalid.
- Enterprise and tenant scope MUST remain explicit and MUST NOT be widened implicitly during application.

## Preconditions and stale state

- A Write MUST validate its expected current version/state before mutation.
- A stale Write Intent MUST NOT overwrite a newer Canonical state.
- Concurrent or conflicting state MUST remain observable as a rejected or deferred application outcome.
- Preconditions MUST be evaluated before Canonical mutation.

## Canonical safety

- Canonical Graph mutation MUST occur only through an explicit governed application step.
- No upstream mapping, identity match, resolution result, or reasoning output MAY implicitly mutate the Canonical Graph.
- A Graph Write MUST NOT create a new canonical entity, attribute, or predicate unless that creation is explicitly authorized by the governing application decision.
- Source-specific semantics MUST NOT enter the Canonical Graph merely because a Write Intent contains them.

## Audit and provenance

- Before-state and intended after-state MUST be recorded for every accepted Write.
- Source identity, provenance, evidence, governing decision, authorization, and application context MUST remain traceable.
- Write History MUST be append-only.
- Historical Write Records MUST NOT be silently rewritten.
- Rejected, deferred, and failed Writes MUST remain observable and attributable.

## Idempotency and replay

- Every Write MUST be idempotent under its declared idempotency key.
- Replaying the same accepted Write Intent MUST NOT produce an unintended additional mutation.
- Application MUST be replayable from the recorded Write Intent, preconditions, decision references, and evidence/provenance context.
- A replay against changed current state MUST re-evaluate preconditions rather than bypass them.

## Failure and partial execution

- A failed or partially executed Write MUST produce an auditable outcome.
- Partial execution MUST NOT be silently reported as successful completion.
- Compensation or recovery MUST be an explicit governed operation and MUST preserve the original Write History.
- Graph availability or transaction failure MUST NOT justify bypassing authorization, preconditions, audit, or provenance requirements.

## Current Truth and history

The current Canonical state MUST remain distinguishable from historical Write Records and Fact Versions. A successful Graph Write MUST reference the Fact Version or lifecycle operation it establishes; it MUST NOT erase the lineage that preceded it.

## Non-goals

This slice does not implement a graph database adapter, transaction engine, authorization service, distributed locking, rollback mechanism, automatic ontology learning, vendor connectors, or unrestricted production ingestion. It defines the governance contract those implementations MUST satisfy.
