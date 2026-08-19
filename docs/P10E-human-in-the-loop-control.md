# P10-E — Human-in-the-loop Control

## Purpose

P10-E provides explicit **review, override, escalation, and delegation** paths
for agent-initiated actions, keeping a human in the loop whenever autonomy is
not full. It composes the P10-D autonomy verdict with the existing S356
authorization governance (approval records and senior overrides).

```text
AutonomyVerdict (P10-D)
   ├─ fully_autonomous -> autonomous path
   ├─ approved         -> approval path (requires explicit human approval)
   ├─ human_review     -> escalation or senior-override path
   └─ blocked          -> rejected unless a senior override is provided
```

## Contract

`src/scm_ontology/human_control.py`:

- **`ControlPath`** — `autonomous` / `approval` / `override` / `escalation` /
  `delegation` / `rejected`.
- **`HumanReviewDecision`** — an explicit human decision (`approve`, `override`,
  `escalate`, `reject`).
- **`route_human_control(...)`** — routes a proposal through the control paths
  and returns an immutable, content-addressed `HumanControlRecord`, optionally
  carrying the `ApprovalRecord` or `DecisionOverride`.

### Control paths

| autonomy verdict | human path | requires |
|---|---|---|
| `fully_autonomous` | autonomous | nothing |
| `approved` | approval / delegation | explicit `approve` + reviewer |
| `human_review` | escalation / override | review decision; senior for override |
| `blocked` | rejected / override | senior override to overturn |

## Fail-closed behavior

- Requires a reviewer for approval and a senior for override.
- A blocked verdict is not overtaken without an explicit senior override.
- Every outcome is recorded (immutable, replayable, content-addressed).

## Guardrails

- P10-E performs no side effect and introduces no new canonical semantics.
- Human governance remains explicit; autonomy is never silently widened.
