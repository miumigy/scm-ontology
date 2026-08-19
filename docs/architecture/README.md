# Architecture Documentation

## Current architecture

- [`current-architecture.md`](./current-architecture.md) — current architecture and layer boundaries

## Current boundary contracts

- [`reasoning-input-boundary.md`](./reasoning-input-boundary.md) — what may enter the reasoning boundary
- [`reasoning-output-boundary.md`](./reasoning-output-boundary.md) — what reasoning may return
- [`proposal-validation-boundary.md`](./proposal-validation-boundary.md) — proposal validation contract
- [`decision-authorization-boundary.md`](./decision-authorization-boundary.md) — decision authorization contract
- [`execution-command-boundary.md`](./execution-command-boundary.md) — immutable governed execution command
- [`decision-context.md`](./decision-context.md) — decision context boundary
- [`decision-proposal.md`](./decision-proposal.md) — decision proposal contract
- [`context-assembly-boundary.md`](./context-assembly-boundary.md) — decision context assembly boundary
- [`context-readiness-boundary.md`](./context-readiness-boundary.md) — decision context readiness boundary
- [`graph-projection-boundary.md`](./graph-projection-boundary.md) — governed graph projection boundary
- [`graph-query-boundary.md`](./graph-query-boundary.md) — governed graph query boundary
- [`graph-observation-boundary.md`](./graph-observation-boundary.md) — graph-to-reasoning observation boundary
- [`reference-canonicalization-boundary.md`](./reference-canonicalization-boundary.md) — reference source-to-canonical boundary
- [`reference-scm-os-flow.md`](./reference-scm-os-flow.md) — reference end-to-end SCM OS flow

## Historical freezes

- [`M4-architecture-freeze.md`](./M4-architecture-freeze.md) — M4 semantic/runtime freeze
- [`v0.2-release-candidate.md`](./v0.2-release-candidate.md) — v0.2 RC historical snapshot
- [`extension-governance.md`](./extension-governance.md) — governed extension lifecycle

## Reading order

```mermaid
flowchart LR
    HIST[Historical Freezes] --> CURRENT[Current Architecture]
    CURRENT --> BOUNDARY[Governed Boundaries]
    BOUNDARY --> IMPL[Post-M8 / v0.1.0 Implementation]
```

Historical documents explain how the architecture evolved. The current
architecture and governed boundary contracts define what a conformant
implementation must satisfy.
