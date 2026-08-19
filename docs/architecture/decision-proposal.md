# S334 — Canonical Decision Proposal Boundary

## Purpose

S334 represents a proposed SCM action without approving or executing it. A proposal references an existing S333 DecisionContext and carries explicit rationale, evidence, and provenance.

## Contract

A `DecisionProposal` contains `decision_id`, `decision_type`, `context_id`, `action`, and `rationale`. Evidence and provenance identifiers are normalized deterministically. JSON uses `contract_version: S334.1`, UTF-8 output, sorted keys, and deterministic separators.

## Semantic boundary

S334 MUST NOT:

- mutate Canonical Truth or graph storage;
- approve or execute an action;
- infer a DecisionContext that was not supplied;
- manufacture rationale, evidence, or provenance;
- perform optimization or planning;
- imply that a proposal has been executed.

The proposal is a governed handoff from SCM reasoning toward human or external execution workflows.