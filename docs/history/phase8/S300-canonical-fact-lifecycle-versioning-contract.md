# S300 — M8 Canonical Fact Lifecycle & Versioning Contract

## Purpose

Define the governed lifecycle of a Canonical Fact so that current Canonical Truth remains distinguishable from historical states, provenance remains intact, and lifecycle changes are explicit, attributable, append-only, and replayable.

## Fact lifecycle

Every Canonical Fact MUST have an explicit lifecycle state. The supported states are:

- `proposed`
- `active`
- `superseded`
- `retired`
- `invalidated`
- `disputed`

A lifecycle transition MUST be explicit, attributable, and governed. A state MUST NOT be inferred merely from the existence of a source observation or a successful mapping.

## Temporal semantics

- Every Fact Version MUST distinguish Effective Time from Recorded Time when those concepts are applicable.
- Effective Time describes when the fact is asserted to hold in the modeled domain.
- Recorded Time describes when the system accepted or recorded the assertion.
- Temporal information MUST NOT be silently normalized away when it affects interpretation of historical truth.
- Overlapping or contradictory temporal assertions MUST remain observable rather than being silently collapsed.

## Version identity and supersession

- Every Canonical Fact Version MUST have a stable, unique version identity.
- A new version MUST NOT overwrite the historical content of a prior version.
- Supersession MUST explicitly identify the prior version being superseded.
- A superseded version MUST remain retrievable as historical state.
- Retired or invalidated facts MUST remain distinguishable from facts that were never asserted.
- A lifecycle transition MUST NOT erase the lineage of preceding versions.

## Canonical truth boundary

- Current Canonical Truth MUST remain distinguishable from historical Fact Versions.
- Historical Fact Versions MUST NOT be silently rewritten to make the current state appear retrospectively correct.
- A lifecycle transition MUST NOT itself create an unrelated Canonical Fact or semantic predicate.
- Provenance, source identity, evidence, enterprise scope, and governing decision references MUST remain attached to each version.
- Conflict or dispute MUST NOT be converted into `active` solely for downstream convenience.

## Provenance and evidence

Every Fact Version MUST preserve the provenance and evidence necessary to explain why the version exists, including the source identity and relevant governed application or resolution decision. Evidence MUST remain distinguishable from Canonical Truth.

## Append-only history

- Fact Version History MUST be append-only.
- Lifecycle Transition Records MUST be append-only.
- Historical Fact Versions MUST NOT be silently rewritten or deleted as a means of correcting current Canonical Truth.
- A correction MUST be represented by a new attributable version or governed lifecycle transition.

## Replay and reconstruction

- Fact lifecycle processing MUST be replayable from recorded versions, transitions, timestamps, provenance, evidence, and governing decisions.
- Replaying historical events MUST reconstruct the historical state without silently applying later knowledge.
- Replaying current state MUST be distinguishable from reconstructing a historical point in time.

## Conflicts and invalidation

Conflicting evidence, disputed assertions, and invalidated facts MUST remain observable and attributable. Invalidation MUST explain the governing reason and MUST NOT erase the invalidated version's historical existence.

## Non-goals

This slice does not define a storage engine, temporal database implementation, transaction protocol, conflict-resolution algorithm, authorization service, ontology-learning mechanism, automatic fact extraction, or vendor-specific lifecycle adapter. It defines the lifecycle and versioning contract those implementations MUST satisfy.
