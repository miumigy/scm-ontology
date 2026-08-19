# P9-G — Phase 9 Acceptance

## Purpose

P9-G closes **Phase 9 (Closed-Loop SCM OS Execution)** with a deterministic
acceptance contract: a reference SCM workflow operates as a governed closed
loop against an injected external system.

P9-G folds the P9-A..P9-F capabilities into an immutable, content-addressed
`Phase9AcceptanceReport` with an overall `accepted` flag.

## Contract

`src/scm_ontology/phase9_acceptance.py`:

- **`run_phase9_acceptance(*, accepted_at)`** — runs the Phase 9 capability
  probes and returns an immutable, content-addressed `Phase9AcceptanceReport`
  with an overall `accepted` flag.
- **`Phase9AcceptanceReport`** — the serialized record (`contract_version:
  P9G.1`, `is_phase9_acceptance: true`, per-capability `operable` +
  `evidence_id`, and a deterministic `report_id`).

### Capability inventory (P9-A..P9-F + the P9-G gate)

| key | slice |
|---|---|
| `execution_outcome_contract` | P9-A — success/failure/partial outcome model |
| `external_execution_adapter` | P9-B — injectable side-effect adapter |
| `approval_to_execution` | P9-C — dry-run to controlled execution |
| `outcome_to_event_canonicalization` | P9-D — governed outcome → canonical event |
| `closed_loop_e2e` | P9-E — full governed closed loop |
| `failure_retry_idempotency` | P9-F — retry, duplicate protection, recovery |
| `governed_closed_loop_gate` | P9-G — ref workflow operates as governed closed loop |

### Phase 9 acceptance criterion

The phase is **accepted** when every P9-A..P9-F capability is operable AND the
`governed_closed_loop_gate` holds:

- a success loop replenishes derived state (5 → 25) via a canonical event whose
  verdict is `success`, proving state → decision → authorization → execution →
  outcome → canonical event → updated state;
- a `no_operation` loop performs no external side effect and leaves state
  unchanged;
- exactly one side effect was recorded against the injected external system
  across both loops (governed execution, not blind writes).

## Fail-closed behavior

- `accepted_at` must be non-empty.
- Any capability probe that raises or returns no usable output is recorded as
  `operable: false` and blocks acceptance (never silently treated as passed).
- The governed closed-loop gate is a hard requirement: if it does not hold, the
  phase is not accepted regardless of the other probes.

## Determinism & provenance

- The same `accepted_at` produces an identical report (`report_id` and JSON).
- Each capability retains an `evidence_id` (content hash of its deterministic
  output) for audit / replay.
- The gate and all probes are deterministic and use the injected
  `ReferenceExternalExecutionAdapter` (no live system).
