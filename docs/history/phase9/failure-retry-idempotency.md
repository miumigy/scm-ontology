# P9-F — Failure / Retry / Idempotency

## Purpose

P9-F adds the reliability semantics a real governed closed loop needs on top of
the P9-C approval-to-execution runtime and the P9-A outcome contract:

- **Idempotency / duplicate protection** — a command id is executed at most once
  against the external system; a duplicate submission returns the recorded
  outcome without re-executing.
- **Bounded retry** — a `failure` outcome is retried up to `max_attempts` with a
  deterministic attempt counter.
- **Partial-execution handling** — a `partial` outcome is recorded and NOT
  retried, so a retry never redoes the already-succeeded portion.
- **Recovery semantics** — when retries are exhausted on a failure, the command
  is marked `failed_permanently` and an explicit `RecoverySignal` (escalation) is
  issued so operators can intervene.

## Contract

`src/scm_ontology/failure_retry_idempotency.py`:

- **`ExecutionAttempt`** — one recorded attempt (attempt number, immutable P9-A
  outcome, timestamp).
- **`ExecutionRunRecord`** — immutable record of all attempts for a command id,
  with a terminal `status` (`executed` / `partial` / `failed_permanently`) and an
  optional `RecoverySignal`.
- **`ExecutionRunRegistry`** — append-only idempotency store keyed by command id;
  refuses overwrites.
- **`RunPolicy(max_attempts)`** — bound on total attempts.
- **`RetryableAdapter`** — deterministic adapter wrapper that can be programmed to
  fail a fixed number of times (or return partial), so retry behavior is testable
  without a flaky live system.
- **`run_with_failure_policy(...)`** — execute with idempotency, bounded retry,
  and recovery semantics.

### Status outcomes

| final outcome | recorded status | recovery signal |
|---|---|---|
| `success` on some attempt | `executed` | no |
| `partial` | `partial` | no (progress made) |
| all attempts `failure` | `failed_permanently` | yes |

## Fail-closed behavior

- `max_attempts` must be `>= 1`.
- A run record with an empty attempt list, or an unknown terminal status, is
  refused.
- The registry refuses to overwrite an already-recorded command id — a duplicate
  submission is replayed, never re-executed.

## Guardrails

- No canonical mutation: every outcome is an immutable P9-A contract, and
  re-execution is governed by the recorded run state.
- Recovery escalates (does not silently succeed) when automatic retries are
  exhausted — never weakening governance to force a green path.
