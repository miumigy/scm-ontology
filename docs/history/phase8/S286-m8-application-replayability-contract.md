# S286 — M8 Application Replayability Contract

## Purpose

Define replayability for governed Canonical Applications without turning replay into an autonomous mutation mechanism.

## Replay Boundary

A replay is a deterministic reconstruction or verification of a previously recorded governed application.

Replay MUST reference the original Application Record and its governing Decision Record.

Replay MUST use the recorded application scope, inputs, provenance, evidence references, and decision context.

Replay MUST NOT silently broaden application scope or introduce newly discovered mappings.

## Safety Invariants

- Reasoning MUST remain read-only.
- Replay MUST NOT create a new canonical entity, attribute, or predicate implicitly.
- Replay MUST NOT mutate canonical facts without an explicit governed application step.
- Replay MUST NOT infer Canonical Truth from replay success alone.
- Replay MUST preserve source identity and provenance.
- Conflicts MUST remain observable.
- Semantic Gap and unresolved identity MUST remain first-class outcomes.
- Vendor-specific semantics MUST NOT enter the Canonical Ontology through replay.

## Determinism and Drift

A replay SHOULD produce an outcome that can be compared with the historical Application Record.

Changes in source data, mapping definitions, Canonical semantics, Decision status, or governance policy MUST be surfaced as replay differences rather than silently rewritten into the historical record.

Historical Application Records MUST remain append-only.

A replay result MUST be recorded separately from the historical Application Record and MUST NOT rewrite it.

## Non-Goals

This contract does not define a replay executor, transaction engine, persistence schema, authorization service, automatic conflict resolution, production graph mutation, or autonomous synchronization.
