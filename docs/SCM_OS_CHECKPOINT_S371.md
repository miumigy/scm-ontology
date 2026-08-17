# SCM OS Checkpoint — S371

S371 closes the first governed decision loop for SCM OS.

```text
Canonical Graph -> Query / Projection -> ReasoningInput -> ReasoningProvider -> ReasoningOutput -> Proposal Validation -> AuthorizedDecision -> ExecutionCommand
```

Reasoning is only a proposal. Authorization is explicit. ExecutionCommand is immutable and has no external side effects. Context, evidence, and provenance are preserved.

S371 intentionally does not implement runtime execution, external side effects, persistence, LLM integration, or UI. Those belong to the next runtime phase.
