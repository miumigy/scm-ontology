# S293 — Governed Application Conflict Contract

## Purpose

Define how conflicts discovered during Identity Resolution Application are represented and contained without silently selecting, discarding, or rewriting Canonical Truth.

## Conflict Requirements

Every material Application conflict MUST remain observable and attributable.

A conflict record MUST preserve:

- the affected source identities
- the relevant Decision and Application Identity
- conflicting evidence and provenance
- the competing proposed values or identities
- the conflict status
- the governing context used for resolution

## Canonical Safety Invariants

- MUST NOT create a new canonical entity, attribute, or predicate automatically as a conflict response.
- MUST NOT mutate canonical facts implicitly.
- MUST NOT silently choose one conflicting source as Canonical Truth.
- MUST NOT silently discard conflicting evidence or provenance.
- Conflicts MUST remain observable.
- Ambiguous and unresolved identity MUST remain first-class outcomes.
- Reasoning MUST remain read-only until an explicit governed Decision and Application step.
- Conflict resolution MUST NOT expand the original Application scope implicitly.

## Resolution Boundary

A conflict MAY be resolved only through an explicit governed Decision that references the conflict record and its supporting evidence.

An unresolved or conflicting result MUST NOT be converted into an accepted Canonical Identity merely because an Application was retried, replayed, or completed technically.

If competing evidence remains unresolved, the conflict MUST remain represented as unresolved rather than being normalized away.

## Historical Integrity

Conflict Records MUST be append-only.

A later resolution, correction, or supersession MUST create a new governed record and MUST NOT silently rewrite the historical conflict or decision.

Replay MUST preserve the original conflict context and MUST produce an observable result.

## Non-Goals

This contract does not define a conflict-scoring algorithm, automatic arbitration, merge strategy, graph transaction implementation, authorization service, or autonomous resolution mechanism.
