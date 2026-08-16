# S332 — Canonical Plan / Actual / Commitment Reconciliation

## Purpose

S332 is a Phase 4 business-question vertical slice that reconciles already-canonical plan, actual, and commitment quantities over an explicit item/period/unit scope.

## Contract

For each exact `(item_id, period_start, period_end, unit)` scope:

- `actual_vs_plan = actual - plan`
- `commitment_vs_plan = commitment - plan`
- `actual_vs_commitment = actual - commitment`

Inputs are canonical facts. Missing fact classes contribute `0` to the derived reconciliation; the runtime does not infer missing business meaning.

## Semantic boundary

S332 MUST NOT:

- perform identity resolution;
- infer that records with different scopes refer to the same item or period;
- change a plan;
- approve or reject a commitment;
- mutate Canonical Truth or graph storage;
- optimize operations;
- recommend corrective action;
- manufacture evidence or provenance.

Evidence and provenance identifiers supplied by the input facts are preserved in the derived result.

## Determinism

Results are sorted by explicit scope. JSON uses `contract_version: S332.1`, UTF-8 output, sorted keys, and deterministic separators.
