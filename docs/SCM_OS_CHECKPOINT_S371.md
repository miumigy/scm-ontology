# SCM OS Checkpoint — S371

S371 defines the first closed governed-decision loop for SCM OS.

## Control loop

Canonical graph observations are projected and assembled into `ReasoningInput`, passed through an engine-neutral `ReasoningProvider`, validated as a decision proposal, explicitly authorized, and finally wrapped as an immutable `ExecutionCommand`.

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

## Safety boundaries

- Reasoning output is a proposal, not an authorization.
- Authorization records actor, authority, and timestamp; it does not execute.
- ExecutionCommand is an immutable envelope; it does not execute anything.
- Evidence and provenance must survive the pipeline.
- Context identity is preserved end-to-end.
- Provider implementations remain replaceable and engine-neutral.

## Deliberate non-goals

S371 does not implement a runtime executor, external side effects, LLM integration, database persistence, or UI. Those belong to the next runtime phase.

## Next phase

Treat this checkpoint as the foundation for SCM OS runtime integration. Future work should attach real query adapters, reasoning providers, authorization policy engines, and execution adapters without weakening the immutable contract boundaries above.
