# S348 — SCM Decision Runtime v0

## Purpose

S348 is the first **Runtime Integration** milestone (Phase R1). It binds the
S333..S346 SCM OS cognitive/governance boundaries into a single deterministic,
in-memory, side-effect-free Python API so the governed decision loop runs as a
runtime rather than as disconnected unit contracts.

The orchestration reuses the existing governed contracts. It does not define a
new canonical semantic boundary.

## Contract

`run_decision_loop(...)` accepts an immutable collection of graph reasoning
observations (`GraphReasoningObservation`), an S368 `ReasoningProvider`, and
explicit authorization/command parameters. It returns an immutable
`DecisionRuntimeResult` carrying every boundary artifact.

The executed path is canonical and must be:

```text
observations -> ReasoningInput -> ReasoningOutput -> ValidatedDecisionProposal
    -> AuthorizedDecision -> ExecutionCommand
```

A `DecisionRuntimeResult` MUST preserve:

- a single `context_id` across reasoning input, output, proposal, authorization, and command;
- the provider `evidence_ids` and `provenance_ids`; and
- the immutable execution command.

The result serializes deterministically with `contract_version: S348.1`,
UTF-8 output, sorted keys, and stable separators.

`MockReasoningProvider` is a deterministic S368 provider implementation used to
exercise the loop without LLM, rule, or optimization backends.

## Non-goals

S348 does not:

- infer business semantics not present in the supplied observations;
- mutate Canonical Truth or graph storage;
- call ERP, WMS, TMS, MES, or other external systems;
- execute the resulting command;
- infer or bypass authorization policy;
- define a rule engine, optimization engine, or LLM provider;
- persist or replay decisions (Runtime Phases R3/R4).

Later runtime phases add provider families (R2), execution and results (R3),
and governance/replay/audit (R4). S348 only sequences the existing
contract boundaries into one auditable runtime call.
