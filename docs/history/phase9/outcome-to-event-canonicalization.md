# P9-D — Outcome-to-Event Canonicalization

## Purpose

P9-D projects a governed execution outcome (the P9-A `ExecutionOutcomeContract`,
as produced through the P9-C approval-to-execution runtime) into a read-only
`CanonicalEvent` that records the outcome as an auditable occurrence — without
bypassing governance.

Up to P9-C, an outcome was an internal record. P9-D is the governed bridge from
execution outcomes back into the Canonical Event stream, which Phase 9's closed
loop uses to close back onto Canonical State (`Canonical Graph -> ... ->
Execution Outcome -> Canonical Event -> Canonical Graph`).

## Contract

`src/scm_ontology/outcome_to_event_canonicalization.py`:

- **`canonicalize_execution_outcome(result, *, event_occurred_at=None) -> CanonicalEvent`** —
  canonicalize a governed `ApprovalToExecutionResult` into an immutable
  `CanonicalEvent` of type `execution_outcome_recorded`.
- **`extract_outcome_canonical_lineage(event) -> dict`** — read-only
  evidence/provenance lineage view (mirrors S349 `CanonicalEventLineage`
  semantics).

### Event attributes

The canonical event embeds the governed path and the outcome provenance:

- `verdict`, `outcome_id`, `executed_at`, and per-target `elements`;
- `governance_command_id`, `governance_state` (`executed`), and the
  `governance_actors` chain from every lifecycle transition;
- `evidence_ids` and `provenance_ids` carried on the outcome.

## Fail-closed behavior

- The input must be an `ApprovalToExecutionResult` from the governed path — a raw
  outcome contract, or any non-governed input, is refused.
- The command lifecycle must have reached the terminal `executed` state; an
  outcome whose lifecycle ended in any other state is never canonicalized.
- `event_occurred_at` (when supplied) must be a timezone-aware ISO-8601
  timestamp.

## Guardrails

- Outcomes never become canonical events by bypassing governance: canonicalization
  is only reachable through the governed approval-to-execution path.
- The produced `CanonicalEvent` is immutable and read-only; it does not mutate
  Canonical Truth — it records the observed outcome so the loop can close.
