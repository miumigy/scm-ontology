# S333 — SCM OS Decision Context Boundary

## Purpose

S333 creates the first SCM OS integration boundary. It bundles already-canonical, derived SCM business-question observations into an immutable decision context for downstream planning, simulation, optimization, or reasoning.

## Contract

A `DecisionContext` contains a unique `context_id` and explicit `DecisionObservation` records. Each observation identifies the business question that produced it and may carry evidence/provenance identifiers supplied by the caller.

JSON uses `contract_version: S333.1`, UTF-8 output, sorted keys, and deterministic separators.

## Semantic boundary

S333 MUST NOT:

- perform source mapping or identity resolution;
- infer observations not supplied by the caller;
- mutate Canonical Truth or graph storage;
- plan, optimize, execute, or recommend an action;
- manufacture evidence or provenance;
- merge observations with duplicate question identifiers.

The context is a read-only handoff into downstream SCM OS capabilities.
