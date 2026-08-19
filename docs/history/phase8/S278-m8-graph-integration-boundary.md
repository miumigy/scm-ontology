# S278 — M8 Canonical Graph Integration Boundary Contract

## Purpose

Define the safety boundary for integrating multiple already-canonicalized enterprise representations into a shared Canonical SCM Graph.

M8 is **not** an extension of the Canonical Ontology. It is a graph-integration contract applied after M7 Canonicalization.

## Integration boundary

```text
Enterprise A ── M7 Canonicalization ──┐
                                      │
Enterprise B ── M7 Canonicalization ──┼──> Canonical Graph Integration
                                      │
Enterprise C ── M7 Canonicalization ──┘             ↓
                                           Shared Canonical SCM Graph
```

Only Canonicalization Results that satisfy the M7 contract may enter this stage.

## Required invariants

1. Graph integration MUST consume explicit Canonicalization Results, not raw enterprise records.
2. Integration MUST NOT create a new canonical entity, attribute, or predicate automatically.
3. Integration MUST NOT mutate canonical facts implicitly as a side effect of identity matching or graph merge.
4. Source identity and provenance MUST remain attached to every integrated result.
5. conflicts MUST remain observable; conflicting source representations MUST remain observable; conflict resolution MUST be explicit and governed.
6. Identity similarity MUST NOT by itself establish Canonical Identity.
7. A shared graph MUST NOT erase enterprise-specific source distinctions needed for provenance or audit.
8. Graph merge MUST be replayable from recorded inputs and governed decisions.
9. Reasoning MUST remain read-only and MUST NOT authorize graph mutation.
10. Semantic Gap and unresolved identity MUST remain first-class outcomes rather than being silently normalized.

## Identity boundary

M8 introduces a distinction between:

- **Source Identity** — identity asserted by an enterprise representation;
- **Candidate Identity Match** — a proposed relationship between source identities;
- **Governed Canonical Identity** — an explicitly approved identity correspondence.

A Candidate Identity Match MUST NOT be treated as a Governed Canonical Identity without an explicit governed application step.

## Conflict boundary

When two canonicalized sources provide incompatible values for the same candidate canonical fact, the integration layer MUST preserve the conflict and its provenance. It MUST NOT silently select a winner merely because one source is newer, more frequent, or technically easier to merge.

## Non-goals

S278 does not implement probabilistic entity resolution, automatic conflict resolution, production multi-tenant ingestion, or autonomous graph mutation. Those concerns require separate contracts and explicit governance.

## Acceptance criterion

M8 graph integration is conformant only when the shared graph preserves canonical semantics, source provenance, unresolved identity, conflicts, and governed mutation boundaries without modifying the Canonical Ontology implicitly.
