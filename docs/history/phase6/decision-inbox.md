# P6-B — Decision Inbox

## Purpose

P6-B is the second **Phase 6 (SCM OS Control Plane)** slice. It provides an
operator-facing **Decision Inbox**: a deterministic projection that lets an
operator *inspect* each governed decision's full inspectable surface —
**proposal, rationale, evidence, provenance, authorization status, and command
state — without recomputing or re-running the decision.**

P6-B composes the already-produced R5 decision results (S358–S362) and the
governed decision chain they carry (a `GovernedExecutionResult` wrapping the
S348 `DecisionRuntimeResult`). It never re-derives a decision, never mutates
Canonical Truth, and performs no external side effect.

## Contract

`build_decision_inbox(decisions, *, viewed_at, viewer_actor_id)` accepts an
iterable of immutable `InboxDecision` values and returns an immutable
`DecisionInbox` with `contract_version: P6B.1` and `is_decision_inbox: true`.

Each `InboxDecision` binds:

- `decision`: one of the signed R5 decisions (Replenishment/Procurement/Production/Distribution);
- `decision_id`: a stable item id;
- `reviewed`: a stateless operator-supplied read flag (the inbox records no mutable read state).

Each projected `InboxItem` exposes:

| field | source |
|---|---|
| `application` | derived decision type |
| `action`, `rationale` | the R5 decision's public fields |
| `status` | `dry_run` when a governed result exists, else `no_action` |
| `context_id`, `actor_id`, `authority`, `authorized_at` | governed decision chain |
| `command_id`, `command_type`, `dry_run_result_id` | governed execution command / dry run |
| `evidence_ids`, `provenance_ids` | governed decision chain (sorted, deduplicated) |
| `reviewed` | the worker-supplied flag |

A `DecisionInbox` folds items into a content-addressed `inbox_id` plus an
`InboxSummary` (item / actionable / no_action / reviewed / unreviewed counts).

## Fail-closed behavior

The inbox MUST reject:

- an empty or non-iterable decision sequence;
- duplicate `decision_id` values;
- an `InboxDecision` whose `decision` is not one of the signed R5 decisions;
- an `InboxDecision` missing a stable `decision_id` or a non-boolean `reviewed`;
- a `decision` missing non-empty `action` / `rationale`;
- blank `viewed_at` / `viewer_actor_id`.

## Determinism & provenance

- The same ordered `InboxDecision` values, `viewed_at`, and `viewer_actor_id`
  produce an identical inbox (`to_json`) and content-addressed `inbox_id`.
- Building the inbox performs zero decision execution: it reads only the
  artifacts already produced by the governed loop.

## Non-goals

P6-B does not:

- recompute, re-run, or authorize any decision;
- mutate Canonical Truth or external systems;
- persist an inbox or record read state (in-memory projection only);
- introduce new canonical Entity, Relationship, or derived-state types.
