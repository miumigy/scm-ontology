# P10-G — Phase 10 Acceptance

## Purpose

P10-G is the acceptance gate for **Phase 10 (Autonomous SCM Control)**. It
folds the P10-A..P10-F capabilities into one deterministic report and closes
the phase when every capability is operable AND a bounded SCM use case remains
governed across the full agent loop:

```text
Observe -> Reason -> Propose -> Simulate -> Evaluate -> Authorize
  -> Execute -> Observe Outcome -> Learn
```

## Contract

`src/scm_ontology/phase10_acceptance.py`:

- **`run_phase10_acceptance(*, accepted_at)`** — runs the seven capability
  probes and returns an immutable, content-addressed `Phase10AcceptanceReport`.
- **`Phase10AcceptanceReport`** — `report_id`, `accepted`, `accepted_at`,
  per-capability `CapabilityResult`s, and an `AcceptanceSummary`.
- Probes cover P10-A..P10-F and the P10-G governed autonomous-loop gate.

### Capabilities probed

| key | name |
|---|---|
| `agent_observation_boundary` | P10-A Agent Observation Boundary |
| `agent_tool_boundary` | P10-B Tool / Action Boundary |
| `simulation_before_execution` | P10-C Simulation-before-Execution |
| `policy_aware_autonomy` | P10-D Policy-aware Autonomy |
| `human_in_loop_control` | P10-E Human-in-the-loop Control |
| `agent_replay_audit` | P10-F Agent Replay / Audit |
| `governed_autonomous_loop_gate` | P10-G Governed Autonomous-Loop Gate |

## Governed autonomous-loop gate

The gate (`_governed_autonomous_loop_gate`) runs a bounded, low-risk,
in-scope, low-impact replenishment proposal through P10-A..P10-F:

- observe a scoped, read-only `AgentObservation`;
- produce an `AgentProposal`;
- evaluate policy-aware autonomy (≥ confidence, ≤ risk, ≤ impact);
- obtain the human-control record (autonomous path);
- record the full lifecycle as a replayable `AgentAuditTrail` and replay it.

The gate holds only when the observation is read-only, autonomy is
fully-autonomous, the control path is autonomous, one audit entry is recorded,
and replay verifies content integrity.

## Fail-closed behavior

- `accepted_at` must be non-empty.
- Any probe failure yields `operable = False` and prevents phase acceptance.
- The gate fails closed if replay detects tampering.

## Guardrails

- P10-G performs no external side effect and never mutates Canonical Truth.
- Autonomy stays a policy-decision result; human governance remains explicit.
