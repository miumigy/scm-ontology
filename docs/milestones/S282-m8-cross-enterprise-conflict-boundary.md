# S282 — M8 Cross-Enterprise Conflict Resolution Boundary

## Purpose

Define how conflicting enterprise representations are retained and escalated without silently selecting a Canonical Truth.

## Conflict model

```text
Enterprise A assertion ─┐
                        ├─ Conflict Set ─→ Governed Resolution Decision
Enterprise B assertion ─┘                         │
                                                   ↓
                                      Canonical application (if approved)
```

A conflict is an observable semantic state, not an instruction to choose one source automatically.

## Required conflict record

A conflict record MUST preserve:

- all materially conflicting source assertions;
- source identity and provenance;
- the canonical concept under consideration, if known;
- conflict type and scope;
- evidence references;
- current resolution status;
- governed decision and rationale, when resolved;
- decision version and timestamp.

## Required outcomes

A conflict MUST support at least:

- **Open** — conflict detected and unresolved;
- **Resolved** — an explicit governed decision exists;
- **Rejected** — a proposed correspondence or assertion was explicitly rejected;
- **Deferred** — resolution intentionally postponed.

## Safety invariants

1. Conflicts MUST remain observable.
2. Conflicting source assertions MUST NOT be silently discarded.
3. The Adapter MUST NOT silently select a winning source.
4. Conflict resolution MUST NOT create a new canonical entity, attribute, or predicate automatically.
5. Conflict resolution MUST NOT mutate canonical facts without an explicit governed application step.
6. Provenance MUST remain attached to every conflicting assertion and resolution decision.
7. A resolution decision MUST be auditable and replayable.
8. Reasoning MUST remain read-only.
9. Unresolved conflicts MUST remain first-class outcomes.
10. Vendor-specific conflict rules MUST remain outside the Canonical Ontology.

## Semantic boundary

Conflict detection identifies incompatible or competing representations. Conflict resolution is a governed decision process. Neither step is itself Canonical Truth creation.

## Non-goals

S282 does not implement automatic source precedence, probabilistic conflict resolution, vendor-specific master-data governance, autonomous canonical mutation, or production reconciliation workflows.
