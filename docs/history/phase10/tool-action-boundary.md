# P10-B — Tool / Action Boundary

## Purpose

P10-B draws the **agent tool boundary**: agents propose actions; they never
perform canonical mutations directly. Agent tools produce scoped observations
(P10-A) and structured, content-addressed `AgentProposal` records that must
still traverse proposal validation (S344) and authorization (S345) before they
may become an `ExecutionCommand`.

```text
Agent tool
  ├─ reads -> P10-A AgentObservation (scoped, evidence-aware, read-only)
  └─ emits -> AgentProposal (content-addressed, evidence-aware)
                 │
                 │ governed path (S344 validate + S345 authorize)
                 ▼
             ExecutionCommand  -> P10-C simulation / P9 execution
```

## Contract

`src/scm_ontology/agent_tool.py`:

- **`AgentProposal`** — an immutable, content-addressed proposed action with
  evidence/provenance/confidence. It carries a `proposal_id` and exposes no
  canonical mutation surface.
- **`AgentToolResult`** — the immutable outcome of invoking an agent tool. It
  holds the read observation and the produced proposal and exposes
  `can_mutate = False`.
- **`run_agent_tool(...)`** — runs a tool's `propose` callable under the
  boundary, requiring it to return an `AgentProposal` (never a mutation).
- **`proposal_to_execution_command(...)`** — routes an `AgentProposal` through
  proposal validation and authorization to build an `ExecutionCommand`. If
  validation or authorization fails, no command is produced.

### Boundaries

| what | allowed |
|---|---|
| agent tool reads | P10-A scoped, evidence-aware observation |
| agent tool emits | `AgentProposal` (proposed action) |
| agent tool mutates canonical graph | **never** |
| proposal becomes command | only via S344 validation + S345 authorization |

## Fail-closed behavior

- `agent_id`, `context_id`, `action`, and `rationale` must be non-empty.
- The tool must return an `AgentProposal` (the boundary rejects any non-proposal
  return value).
- The proposal flows through the governed decision layer; an unauthorized or
  unvalidated proposal never becomes an `ExecutionCommand`.

## Guardrails

- P10-B performs no side effect and introduces no new canonical semantics.
- The agent's reach is bounded to read + propose; execution remains the job of
  the governed execution layer (P9).
