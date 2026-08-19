# P10-F — Agent Replay / Audit

## Purpose

P10-F makes every agent lifecycle step **replayable**: observation, proposal,
decision, authorization, command, and outcome are recorded as an immutable,
content-addressed, append-only audit trail that can be replayed to prove
reproducibility and detect tampering.

```text
AgentObservation -> AgentProposal -> AutonomyVerdict
  -> HumanControlRecord -> ExecutionCommand -> outcome
       (all recorded as one content-addressed AgentAuditEntry)
```

## Contract

`src/scm_ontology/agent_replay.py`:

- **`AgentAuditEntry`** — an immutable, content-addressed record of one agent
  lifecycle step carrying the observation, proposal, autonomy verdict, human
  control record, command, and outcome reference.
- **`AgentAuditTrail`** — an append-only, immutable trail of entries for one
  agent.
- **`record_agent_entry(...)`** — records a step and computes its
  content-addressed `entry_id`.
- **`AgentAuditTrail.record(...)`** — returns a new trail with one more entry
  (the original is unchanged).
- **`AgentAuditTrail.replay()`** — recomputes each entry's content address and
  verifies it matches the recorded `entry_id`; tampering raises
  `AgentReplayError`.

### Replay integrity

- Each `entry_id` is a deterministic hash of the full entry payload.
- Replay recomputes the hash; any change to the entry is detected.
- The trail is append-only: building the same sequence deterministically yields
  an identical trail, and the original trail is never mutated.

## Fail-closed behavior

- `agent_id` must be non-empty.
- All entries in a trail must belong to the same agent.
- A content-integrity mismatch on replay raises rather than silently passing.

## Guardrails

- P10-F performs no side effect and introduces no new canonical semantics.
- It only persists an auditable, replayable record of the governed agent path.
