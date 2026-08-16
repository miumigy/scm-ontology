# S344 — Decision Proposal Validation Boundary

S344 validates a `ReasoningOutput` before it can enter a future authorization or execution layer.

## Boundary

```text
S342 ReasoningInput
        ↓
   Reasoning Engine
        ↓
S343 ReasoningOutput
        ↓
S344 Proposal Validation
        ↓
ValidatedDecisionProposal
        ↓
Future authorization / execution
```

## Rules

- `context_id` must match the reasoning input.
- `proposal` must be non-empty.
- Evidence and provenance must be present.
- Evidence/provenance identifiers must originate in the reasoning input.
- The original `ReasoningOutput` is immutable and is not modified.
- Validation does not authorize, execute, or infer a decision.

This boundary deliberately separates AI reasoning from decision authorization and execution.
