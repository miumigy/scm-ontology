# S292 — Identity Application Idempotency Contract

## Purpose

Define the idempotency boundary for governed Identity Resolution Applications so that retries and replay do not silently create duplicate Canonical changes or rewrite historical Application Records.

## Idempotency Key

Every governed Identity Resolution Application MUST carry a stable Application Identity that uniquely identifies the intended governed operation within its scope.

A retry of the same Application Identity MUST be distinguishable from a new governed Application.

Idempotency MUST be evaluated together with the governing Decision, application scope, target Canonical Identity, and intended change. A matching identifier MUST NOT authorize a different mutation.

## Canonical Safety Invariants

- MUST NOT create a new canonical entity, attribute, or predicate automatically outside the governed Application.
- MUST NOT mutate canonical facts implicitly.
- MUST NOT treat retry success as evidence of new Canonical Truth.
- Conflicts MUST remain observable.
- Source identity and provenance MUST remain attached.
- Semantic Gap and unresolved identity MUST remain first-class outcomes.
- Reasoning MUST remain read-only.
- An idempotent replay MUST NOT silently expand the original Application scope.

## Retry and Replay Semantics

A repeated Application Identity MUST resolve to the existing Application outcome or an explicit governed retry outcome according to policy.

A retry MUST NOT silently execute a different Canonical change.

Replay MUST produce a distinct observable execution result while preserving the historical Application Record.

If relevant inputs, evidence, Decision, governance context, or target identity have drifted, the result MUST expose the drift rather than silently treating the execution as identical.

## Historical Integrity

Application Records MUST be append-only.

Idempotency MUST NOT be implemented by silently rewriting, deleting, or collapsing historical Application Records.

Any corrected or materially different operation MUST receive a new governed Application Identity and an auditable record.

## Non-Goals

This contract does not define a storage implementation, distributed locking algorithm, transaction protocol, graph database mechanism, authorization service, automatic retry scheduler, or production synchronization mechanism.
