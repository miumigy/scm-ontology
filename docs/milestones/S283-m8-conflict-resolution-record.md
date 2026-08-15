# S283 — M8 Conflict Resolution Decision Record

## Purpose

Define the governed decision record required before an enterprise conflict may be applied to Canonical Identity or Canonical Facts.

## Decision lifecycle

```text
Conflict Set
    ↓
Decision Proposal
    ↓
Governed Review
    ↓
Decision Record
    ↓
Explicit Application (if approved)
```

A Decision Record records a decision; it does not itself mutate the Canonical Graph.

## Required fields

A Decision Record MUST preserve:

- decision identifier;
- conflict-set identifier;
- affected source identities and assertions;
- evidence and provenance references;
- proposed resolution;
- decision status;
- decision rationale;
- governing authority or actor;
- decision version;
- created and effective timestamps.

## Decision statuses

At minimum:

- **Proposed** — awaiting governed review;
- **Approved** — explicitly authorized for application;
- **Rejected** — explicitly declined;
- **Superseded** — replaced by a later decision.

## Safety invariants

1. Decision history MUST be append-only.
2. Historical decisions MUST NOT be silently rewritten.
3. An Approved decision MUST NOT mutate canonical facts by itself; application MUST be an explicit governed step.
4. Rejected, superseded, and proposed decisions MUST remain observable.
5. Evidence and provenance MUST remain attached to the decision.
6. A decision MUST NOT infer Canonical Truth from provenance alone.
7. Decision rationale MUST be auditable and replayable.
8. Reasoning MUST remain read-only.
9. Vendor-specific governance rules MUST remain outside the Canonical Ontology.

## Boundary

The Decision Record is governance metadata around a proposed semantic resolution. It is not a Canonical Fact and must not be treated as one merely because it has been approved.

## Non-goals

S283 does not implement approval workflows, user authorization, automatic conflict resolution, graph mutation, or production master-data synchronization.
