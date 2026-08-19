# P9-B — External Execution Adapter

## Purpose

P9-B introduces the bounded boundary through which a governed
`ExecutionCommand` may actually cause side effects in an external system
(ERP / WMS / TMS / MES). Up to and including Phase 8, execution was
side-effect-free dry-run only (`execute_dry_run`). P9-B defines the
`ExternalExecutionAdapter` protocol whose `execute` performs the side effect and
returns a deterministic `ExecutionOutcomeContract` (P9-A).

A live ERP/WMS connector is implemented later against this same boundary; the
delivered `ReferenceExternalExecutionAdapter` is a deterministic test double that
simulates an external system against an in-memory order book, so tests and the
closed-loop E2E exercise real side effects reproducibly with no live system.

## Contract

`src/scm_ontology/external_execution_adapter.py`:

- **`ExternalExecutionAdapter`** (Protocol) — `adapter_id`, `supports(command_type)`,
  and `execute(command, *, executed_at, external_system) -> ExecutionOutcomeContract`.
- **`validate_external_adapter(adapter)`** — fail-closed boundary check.
- **`InMemoryExternalSystem`** — minimal stand-in recording every side effect
  received; carries no SCM semantics and is not canonical state.
- **`ReferenceExternalExecutionAdapter`** — deterministic test double supporting
  the R5/Phase 5 command types (replenishment, procurement, production,
  distribution) whose outcome is derived entirely from the command content.
- **`execute_externally(command, *, adapter, executed_at, external_system)`** —
  validate the adapter, check command-type support, perform the side effect, and
  return the immutable outcome contract.

### Deterministic outcome control (test double)

| proposal flag | outcome |
|---|---|
| (none) | `success` — one successful element |
| `simulate_failure: true` | `failure` — one failing element |
| `simulate_partial: true` | `partial` — one success + one failure element |

Each produced element is also written to the injected `InMemoryExternalSystem`
so tests can assert the side effect actually occurred.

## Fail-closed behavior

- The adapter must expose a non-empty `adapter_id`, a callable `supports`, and a
  callable `execute`.
- The adapter must support the command type or execution is refused.
- `execute` must return an `ExecutionOutcomeContract` (never a raw mapping).
- Errors raised inside the adapter are wrapped, never silently swallowed.

## Guardrails

- Executing through this adapter MAY cause side effects in an external system —
  that is its purpose — but it never mutates Canonical Truth directly; the
  outcome is captured only as an immutable P9-A contract.
- The boundary is injectable: production adapters implement the same protocol.
