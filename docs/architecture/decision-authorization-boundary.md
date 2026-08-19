# S345 — Decision Authorization Boundary

S345 records authorization of an already validated decision proposal.

```text
S342 ReasoningInput
      ↓
Reasoning Engine
      ↓
S343 ReasoningOutput
      ↓
S344 ValidatedDecisionProposal
      ↓
S345 AuthorizedDecision
      ↓
Future Execution
```

## Contract

`AuthorizedDecision` contains:

- the validated proposal
- `actor_id`
- `authority`
- `authorized_at`
- inherited evidence IDs
- inherited provenance IDs
- contract version `S345.1`

All fields are immutable.

## Boundary rules

- Only a `ValidatedDecisionProposal` can be authorized.
- Actor identity, authority, and authorization timestamp must be non-empty.
- Authorization does not mutate the proposal.
- Authorization does not execute the proposal.
- Authorization does not perform inference or policy evaluation.
- Evidence and provenance remain attached to the authorized result.

S345 therefore separates **decision authorization** from both **AI reasoning** and **execution**.
