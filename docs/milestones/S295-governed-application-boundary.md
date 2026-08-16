# S295 — Governed Canonical Application Boundary

## Purpose

Define the final governance boundary between a completed Resolution and an explicit Application that may change Canonical state.

## Application Preconditions

A Canonical Application MUST reference:

- the Resolution Record
- the governing Decision
- the target Canonical facts or graph scope
- the evidence and provenance supporting the Decision
- the authorization or policy context
- the expected pre-application state
- an idempotency key or equivalent replay identity

An Application MUST be rejected or remain pending when any required precondition is missing, stale, ambiguous, unauthorized, or inconsistent with the recorded Decision.

## Explicit Application Boundary

- A Resolution MUST NOT itself mutate Canonical facts.
- Canonical mutation MUST occur only through an explicit governed Application step.
- The Application scope MUST be explicit and MUST NOT expand implicitly from related evidence or mappings.
- Application authorization MUST be attributable to the governing Decision and policy context.
- Reasoning and mapping MUST remain read-only until the Application boundary is crossed.

## State and Concurrency Safety

Before mutation, the Application MUST validate that the expected pre-application state still holds.

A stale or conflicting state MUST cause rejection or a new governed Decision; it MUST NOT be silently overwritten.

The Application MUST define observable before-state and intended after-state information sufficient to audit what was authorized.

## Idempotency and Replay

Repeated submission of the same Application identity MUST NOT produce additional Canonical mutations beyond the governed result of the original Application.

Application execution MUST be replayable from its recorded inputs, Decision, scope, governance context, and execution identity.

Replay MUST preserve the original Application history and MUST NOT silently rewrite prior results.

## Failure and Compensation

A failed Application MUST produce an observable failure outcome with sufficient context for audit and replay.

Partial execution MUST NOT be represented as successful completion. Any compensation, retry, or corrective action MUST be explicit, governed, and historically attributable.

Rollback or compensation MUST NOT silently erase the original Application record or its evidence.

## Audit Invariants

Application history MUST be append-only.

The system MUST preserve Decision, Application identity, scope, provenance, before-state, intended after-state, outcome, and relevant execution metadata.

Conflicts, unresolved identity, rejected Applications, and authorization failures MUST remain observable outcomes.

## Non-Goals

This contract does not define a specific graph database transaction API, authorization implementation, distributed transaction protocol, merge algorithm, automatic retry policy, rollback mechanism, or autonomous Canonical mutation.
