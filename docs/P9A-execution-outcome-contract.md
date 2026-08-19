# P9-A — Execution Outcome Contract

## Purpose

P9-A establishes the explicit outcome contract for governed **real** execution:
a command may produce one or more per-target results, each carrying its own
status, evidence, and external reference, which are aggregated into a phase
verdict (`success` / `partial` / `failure` / `rejected`).

This extends the S347/S348 outcome foundation (`execution_outcome.py`,
`execution_outcome_event.py`) that only modelled a single scalar status. It is
the deterministic, content-addressed boundary that P9-B (external execution
adapter), P9-C (approval-to-execution runtime), P9-D (outcome-to-event
canonicalization) and the phase acceptance build on.

## Contract

`src/scm_ontology/execution_outcome_contract.py`:

- **`ResultElement`** — immutable per-target result: `target_ref`, `status`
  (`success` or `failure`), optional `external_reference` and `detail`.
- **`ExecutionOutcomeContract`** — immutable, content-addressed outcome record
  bound to an `ExecutionCommand`, with a derived phase `verdict` and explicit
  `evidence_ids` / `provenance_ids` on the record itself.
- **`build_execution_outcome_contract(...)`** — derive the verdict from the
  element set unless an explicit verdict is supplied.
- **`reject_execution_outcome_contract(...)`** — record that no side effect was
  attempted (governance / adapter declined) as a `rejected` verdict with no
  elements.

### Verdict semantics

| condition | verdict |
|---|---|
| every element succeeded | `success` |
| at least one succeeded and at least one failed | `partial` |
| every element failed (none succeeded) | `failure` |
| no side effect attempted | `rejected` |

## Fail-closed behavior

- A `rejected` verdict may not carry execution elements; any other verdict must
  carry a non-empty element set.
- Element status must be `success` or `failure`; verdict must be one of the four
  phase statuses.
- An explicitly supplied verdict that is inconsistent with the element set is
  rejected (never silently corrected).
- `evidence_ids` / `provenance_ids` must contain non-empty identifiers only.

## Determinism & provenance

- `outcome_id` is the SHA-256 content digest of the command, verdict, elements,
  evidence, and provenance — but **excludes** the wall-clock `recorded_at`,
  matching the governed-audit pattern so replay stays reproducible.
- The same content produces an identical `outcome_id`, `to_mapping()`, and
  `to_json()`.
- The outcome is immutable; it records an observed result and performs no side
  effect and never mutates Canonical Truth.
