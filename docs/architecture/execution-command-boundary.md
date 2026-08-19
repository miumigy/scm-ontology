# S346 — Execution Command Boundary

S346 defines the canonical boundary between an authorized decision and a future execution adapter.

## Contract

`ExecutionCommand` may only be constructed from an `AuthorizedDecision`.

It carries:

- command identity and type
- context identity
- decision proposal
- authorization actor, authority, and timestamp
- evidence and provenance identifiers
- contract version

The command is immutable and deterministic when serialized.

## Non-goals

S346 does not:

- call ERP, WMS, TMS, MES, or other external systems
- mutate domain state
- infer authorization policy
- execute the command
- convert an unauthorized proposal into a command

The intended future flow is:

`AuthorizedDecision -> ExecutionCommand -> Execution Adapter -> External System`
