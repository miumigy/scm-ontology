# S354 — Governed Decision Audit Trail & Replay

## Purpose

S354 is the first **Governance** milestone (Phase R4). It records one governed
decision run as a content-addressed audit entry and replays the deterministic
governed chain to prove the record is reproducible and tamper-evident.

It reuses the S348 decision runtime and, optionally, the S353 execution
runtime. It introduces no new canonical semantics and never performs an
external side effect.

## Contract

`record_governed_decision(result, *, recorded_at, dry_run)` returns an
immutable `GovernedDecisionAuditEntry` whose `audit_id` is the deterministic
hash of the serialized decision (and optional dry run). The entry bundles:

- `result` — the S348 `DecisionRuntimeResult` (reasoning, validation, authorization, command);
- `dry_run` — the optional S353 `DryRunExecutionResult`;
- `context_id` and `command_id`.

`build_audit_trail(entries)` returns an immutable, ordered `GovernedAuditTrail`
(`contract_version: S354.2`).

`replay_governed_decision(entry, ...)` re-runs the **deterministic** governance
steps — proposal validation, authorization, and command construction — and
fails closed unless the reproduced artifacts match the recorded decision and
the content digest is unchanged.

## Non-goals

S354 does not:

- re-run the reasoning provider (LLM and solvers are not deterministic);
- mutate Canonical Truth or any external system;
- infer or bypass authorization policy;
- perform the execution.
