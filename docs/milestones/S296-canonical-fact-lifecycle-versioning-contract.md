# S296 — Canonical Fact Lifecycle / Versioning Contract

## Purpose

Define the governed lifecycle of a Canonical Fact after an explicit Canonical Application is authorized. A Canonical Fact is never an unversioned mutable value: every accepted state is represented by an immutable Fact Version with traceable lineage.

## Core model

A Canonical Fact MUST have a stable Fact Identity independent of its versions. Each accepted state MUST have a distinct Fact Version Identity and MUST identify its predecessor when one exists.

The lifecycle MUST distinguish at least:

- Fact Identity
- Fact Version Identity
- predecessor and successor relationships
- current version
- historical version
- observed time
- effective time
- recorded time
- source identity
- provenance and evidence
- governing Application / Decision
- lifecycle status

Historical versions MUST remain immutable. A new state MUST be represented by a new version rather than by rewriting an existing version.

## Canonical truth boundary

Creating, superseding, accepting, rejecting, or retiring a Fact Version MUST NOT silently create a new Canonical entity, attribute, or predicate.

MUST NOT mutate an existing historical Fact Version.

MUST NOT overwrite historical Canonical Truth in place.

MUST NOT infer Canonical Truth merely because a newer source observation exists.

A new Canonical Fact Version MUST arise only from an explicit governed Canonical Application.

Version creation MUST preserve the Application scope and MUST NOT implicitly expand the set of Canonical Facts being changed.

## Lifecycle semantics

A Fact Version MAY be proposed, accepted, superseded, retired, rejected, or otherwise governed according to an explicit lifecycle policy. A rejected or superseded version remains part of history and MUST NOT be silently deleted.

The current version MUST be derivable from explicit lifecycle state and lineage. Historical versions MUST remain queryable for audit and replay.

Supersession MUST identify both the predecessor and successor. Supersession MUST NOT rewrite the predecessor's historical contents.

## Temporal semantics

Observed time describes when the source observation was made. Effective time describes when the fact is intended to be true in the modeled domain. Recorded time describes when the governed Canonical Application recorded the version.

These timestamps MUST NOT be conflated. A late-arriving observation MUST NOT silently rewrite the temporal history of an existing version.

## Provenance and evidence

Source identity, provenance, and evidence MUST remain attached to each Fact Version. A version MUST NOT inherit provenance merely by position in the version chain when the governing evidence differs.

Conflicting evidence MUST remain observable. Semantic Gap and unresolved identity MUST remain valid outcomes and MUST NOT be converted into a Canonical Fact Version without explicit governance.

## Audit and history

Fact Version history MUST be append-only.

MUST NOT silently rewrite historical Fact Versions, lineage, provenance, or lifecycle decisions.

Every version transition MUST be attributable to its governing Application and Decision.

Version history MUST be replayable from immutable records.

Audit records MUST preserve before-version, intended successor version, actor or authorization context, evidence/provenance references, and transition outcome.

## Idempotency and concurrency

Repeated execution of the same governed Application MUST NOT create duplicate Fact Versions when the application identity and expected state are unchanged.

An Application based on stale expected state MUST be rejected or explicitly re-governed; it MUST NOT silently overwrite a newer version.

Concurrent version creation MUST preserve a single observable lineage. Conflicting successor attempts MUST remain observable as conflicts rather than being silently discarded.

## Read and write boundaries

Reasoning, mapping, evidence evaluation, and version selection MUST remain read-only until an explicit governed Application step.

The lifecycle contract does not itself implement graph transactions, authorization, distributed locking, merge algorithms, automatic conflict arbitration, rollback execution, or autonomous Canonical mutation.

## Acceptance criteria

S296 is satisfied when the Canonical Fact lifecycle is explicitly versioned, historical versions are immutable and append-only, temporal semantics are distinct, provenance/evidence remain attached, stale writes cannot silently overwrite newer truth, and every accepted transition is attributable and replayable.
