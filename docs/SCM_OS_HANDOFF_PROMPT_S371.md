# SCM OS — New Session Handoff Prompt

You are the continuing implementation AI for the user's `miumigy/scm-ontology` project.

## Mission

Build SCM OS as a governed supply-chain decision system. The ontology is not merely a data model: it provides canonical truth, deterministic query/projection boundaries, reasoning contracts, governance, authorization, and execution-command contracts.

## Current checkpoint

S371 is the first closed governed-decision loop:

```text
Canonical Graph
  -> Query / Projection
  -> ReasoningInput
  -> ReasoningProvider
  -> ReasoningOutput
  -> Proposal Validation
  -> AuthorizedDecision
  -> ExecutionCommand
```

The loop is contractually connected by immutable/fail-closed boundaries. S371 deliberately does not execute external side effects.

## Important existing contracts

- `graph_query.py`: canonical graph query boundary
- `graph_projection.py`: deterministic graph projection
- `graph_reasoning_projection.py`: S366 graph -> reasoning observation
- `reasoning_assembly.py`: S367 observations -> ReasoningInput
- `reasoning_provider.py`: S368 engine-neutral provider boundary
- `reasoning_output.py`: S343 immutable reasoning proposal output
- `proposal_validation.py`: S344 proposal governance boundary
- `decision_authorization.py`: S345 explicit authorization boundary
- `execution_command.py`: S346 immutable execution-command envelope

Do not casually redesign these contracts. Prefer additive, backward-compatible evolution and inspect `main` before implementing a new Sxxx task because work may already have landed.

## Recent lessons

1. CI failures have often been caused by stale branches or duplicated Sxxx implementations after the target functionality already landed on `main`.
2. Always inspect current `main` before creating a new implementation.
3. Avoid introducing compatibility aliases merely to satisfy stale tests when the canonical contract has intentionally changed; update the test or build the next boundary from the current contract.
4. When conflicts occur, recreate the work from current `main` rather than trying to preserve an obsolete branch.
5. Keep CI green after every merge.

## S371 acceptance condition

The integration test demonstrates deterministic end-to-end propagation of:
- context_id
- proposal
- evidence_ids
- provenance_ids
- actor_id
- authority
- authorization timestamp
- command identity/type

No external side effect is permitted by the S371 command envelope.

## Where to go next

Stop and reassess architecture before adding many more Sxxx contracts. The next phase should be runtime integration, not endless contract proliferation. Candidate work:

1. real Canonical Graph query adapter
2. real reasoning-provider adapters (LLM/rules/optimization)
3. explicit authorization policy evaluation
4. execution adapter with idempotency/dry-run/audit semantics
5. persistent audit trail
6. SCM OS operational API/UI
7. end-to-end acceptance smoke test

The key architectural principle is:

**AI may propose; governance authorizes; execution adapters perform side effects.**

At the beginning of a new session, inspect the latest `main`, verify CI status, inspect open PRs, then choose the smallest next runtime milestone. Do not assume an Sxxx is missing solely from historical conversation context.
