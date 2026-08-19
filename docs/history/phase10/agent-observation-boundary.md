# P10-A — Agent Observation Boundary

## Purpose

P10-A is the first Phase 10 milestone. It draws an explicit **read boundary**
for agents: an agent receives scoped, evidence-aware observations rather than
unrestricted graph mutation access.

The lesson from the governed layer is that AI must be a **Reasoning Provider /
Agent**, not the owner of Canonical Truth. Agent tools must never mutate the
canonical graph directly. P10-A makes the observation surface explicit and
auditable before any reasoning begins.

```text
Canonical Projection (S337)
        ↓  S338 graph query (scoped)
Scoped GraphQueryResult
        ↓  S339 projection
GraphReasoningObservation
        ↓  P10-A envelope (immutable, content-addressed, can_write=False)
AgentObservation  -> agent reasoning
```

## Contract

`src/scm_ontology/agent_observation.py`:

- **`AgentScope`** — the bounded read scope granted to one agent for one
  question (`agent_id`, `question_id`, optional `node_type`, `node_id`,
  `relationship_type`).
- **`AgentObservation`** — immutable, content-addressed observation delivered
  to the agent. It embeds the `AgentScope` and the `GraphReasoningObservation`,
  and exposes `can_write = False`.
- **`build_agent_observation(...)`** — constructs the scoped observation from an
  already-validated `GraphProjection` through the existing S338/S339 read path.

### Properties

| property | value |
|---|---|
| read-only | always (`can_write = False`, no mutation method) |
| scope | explicit filters (`node_type`, `node_id`, `relationship_type`) |
| deterministic | identical input → identical `observation_id`/JSON |
| evidence-aware | carries the projection's `provenance_ids` |
| content-addressed | `observation_id` hashes scope + observation payload |

## Fail-closed behavior

- `question_id` and `agent_id` must be non-empty.
- The source must be an already-validated `GraphProjection`.
- The observation always applies the exact scope as a deterministic graph query;
  it never returns more than the requested filters.

## Guardrails

- P10-A performs no mutation and introduces no new canonical semantics.
- Agent reasoning never receives a write surface through this boundary; any
  agent-proposed action must instead flow through the P10-B proposal/command
  boundary and remain governed.
