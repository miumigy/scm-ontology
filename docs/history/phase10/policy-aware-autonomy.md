# P10-D — Policy-aware Autonomy

## Purpose

P10-D makes autonomy a **policy decision**, not an implicit property of an AI
model. It composes explicit proposal factors — confidence, risk, monetary
impact, operational scope — with a declarative approval policy to determine the
allowed autonomy level for an agent-initiated action.

```text
AgentProposal
   ├─ confidence, risk, monetary_impact, scope
   └─ AutonomyPolicy (max autonomy per scope + thresholds)
               ↓
      AutonomyVerdict (content-addressed, deterministic)
```

## Contract

`src/scm_ontology/policy_autonomy.py`:

- **`AutonomyLevel`** — `fully_autonomous` > `approved` > `human_review` >
  `blocked`.
- **`AutonomyInput`** — explicit confidence, risk, monetary impact, and scope
  factors.
- **`AutonomyPolicy`** — declarative policy: allowed autonomy per scope,
  monetary-impact limit, confidence threshold, and risk threshold.
- **`evaluate_autonomy(...)`** — computes the deterministic
  `AutonomyVerdict` from the proposal, inputs, and policy.

### Verdict matrix (fail closed)

| factor | effect |
|---|---|
| confidence below threshold | `blocked` |
| risk above threshold | `human_review` |
| monetary impact above limit | `approved` |
| unknown scope | `blocked` |
| all within limits | scope-limited best autonomy level |

## Fail-closed behavior

- Inputs outside [0,1] (confidence/risk), negative impact, or blank scope raise.
- An unknown scope is denied, never silently broadened.
- P10-D only informs governance; it never authorizes or executes.

## Guardrails

- Autonomy stays a policy result; human governance remains explicit.
- P10-D performs no side effect and introduces no new canonical semantics.
