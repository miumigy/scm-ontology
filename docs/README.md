# SCM Ontology Documentation

This is the **product documentation index** for SCM Ontology. It is organized by
semantic area rather than by development number, so that a new reader can find the
current architecture, the semantic contract, the governed runtime, and the
development history without following a sequence of milestone identifiers.

## Primary Launch (SCM Ontology v0.1.0 / SCM OS Reference v0.1.0)

The public launch surface is intentionally small and self-contained.

- [`launch/README.md`](launch/README.md) — primary-launch documentation index
- [`launch/primary-launch.md`](launch/primary-launch.md) — what is released and what is not claimed
- [`launch/golden-path.md`](launch/golden-path.md) — the executable Golden Path
- [`launch/acceptance.md`](launch/acceptance.md) — the machine-executable L5 acceptance gate
- [`launch/demo.md`](launch/demo.md) — a multi-source ERP + WMS + TMS reference example
- [`launch/release-notes-v0.1.0.md`](launch/release-notes-v0.1.0.md) — v0.1.0 release notes
- [`primary-launch-handoff.md`](primary-launch-handoff.md) — authoritative v0.1.0 handoff

## Current architecture

- [`architecture/current-architecture.md`](architecture/current-architecture.md) — current architecture and layer boundaries
- [`architecture/reasoning-input-boundary.md`](architecture/reasoning-input-boundary.md) — reference reasoning input boundary
- [`architecture/reasoning-output-boundary.md`](architecture/reasoning-output-boundary.md) — reference reasoning output boundary
- [`architecture/proposal-validation-boundary.md`](architecture/proposal-validation-boundary.md) — proposal validation boundary
- [`architecture/decision-authorization-boundary.md`](architecture/decision-authorization-boundary.md) — decision authorization boundary
- [`architecture/execution-command-boundary.md`](architecture/execution-command-boundary.md) — governed execution command boundary
- [`architecture/decision-context.md`](architecture/decision-context.md) — decision context boundary
- [`architecture/decision-proposal.md`](architecture/decision-proposal.md) — decision proposal contract
- [`architecture/graph-projection-boundary.md`](architecture/graph-projection-boundary.md) — governed graph projection boundary
- [`architecture/graph-query-boundary.md`](architecture/graph-query-boundary.md) — governed graph query boundary
- [`architecture/graph-observation-boundary.md`](architecture/graph-observation-boundary.md) — graph-to-reasoning observation boundary
- [`architecture/context-assembly-boundary.md`](architecture/context-assembly-boundary.md) — decision context assembly boundary
- [`architecture/context-readiness-boundary.md`](architecture/context-readiness-boundary.md) — decision context readiness boundary
- [`architecture/reference-canonicalization-boundary.md`](architecture/reference-canonicalization-boundary.md) — reference source-to-canonical boundary
- [`architecture/reference-scm-os-flow.md`](architecture/reference-scm-os-flow.md) — reference end-to-end SCM OS flow

## SCM semantics

The canonical semantic model and its reasoning contracts live under
[`semantics/`](semantics/). These are the normative semantic specifications for
the current model. Each file describes one semantic contract; the filename is a
stable historical identifier and is not a development-planning sequence to be
extended.

## Operations (SCM OS Reference runtime)

The governed runtime contracts and applications live under
[`operations/`](operations/). They describe how the model is executed through
the governed decision loop.

- [`operations/decision-runtime.md`](operations/decision-runtime.md) — the governed in-memory decision runtime
- [`operations/rule-reasoning-provider.md`](operations/rule-reasoning-provider.md) — deterministic rule-based reasoning provider
- [`operations/llm-reasoning-provider.md`](operations/llm-reasoning-provider.md) — injected, transport-neutral LLM provider
- [`operations/execution-runtime.md`](operations/execution-runtime.md) — in-memory, side-effect-free execution runtime
- [`operations/governed-audit.md`](operations/governed-audit.md) — governed audit trail & replay
- [`operations/command-lifecycle.md`](operations/command-lifecycle.md) — immutable command lifecycle state machine
- [`operations/authorization-governance.md`](operations/authorization-governance.md) — authorization policy, approval & override
- [`operations/replenishment-application.md`](operations/replenishment-application.md) — replenishment decision application
- [`operations/procurement-application.md`](operations/procurement-application.md) — procurement decision application
- [`operations/production-application.md`](operations/production-application.md) — production decision application
- [`operations/distribution-application.md`](operations/distribution-application.md) — distribution decision application
- [`operations/governed-simulation.md`](operations/governed-simulation.md) — multi-period governed simulation
- [`operations/optimized-planning.md`](operations/optimized-planning.md) — optimized multi-period replenishment planning
- [`operations/optimized-app-planning.md`](operations/optimized-app-planning.md) — optimized procurement / production / distribution planning
- [`operations/operational-workflow.md`](operations/operational-workflow.md) — operational workflow & reporting
- Business-question slices (inventory position, demand/supply gap, multi-hop risk, capacity, disruption propagation) are under [`operations/`](operations/).

## Reference material

- [`reference/canonicalization.md`](reference/canonicalization.md) — reference source-to-canonicalization boundary
- [`reference/canonicalization-pipeline.md`](reference/canonicalization-pipeline.md) — reference canonicalization pipeline contract

## Development history

Development history lives under [`history/`](history/) and is **not** the current
product surface:

- [`history/README.md`](history/README.md) — orientation for the development archive
- [`history/post-m8-roadmap.md`](history/post-m8-roadmap.md) — the Phase 6–10 post-M8 development roadmap
- interested readers who want the "why" of the design should start here, then move
  to [`semantics/`](semantics/).

## Reading the contracts

The word **MUST** is normative. A future implementation that violates a MUST is
non-conformant even if it is convenient, fast, or technically successful.

Contracts are intentionally implementation-neutral. Database choice, graph
engine, scheduler, queue, authorization product, API style, and deployment
topology are implementation decisions that must conform to the semantic
contracts.

## Documentation maintenance rule

When a contract changes, update:

1. the normative contract;
2. its regression tests;
3. the relevant architecture/index document;
4. the README if the conceptual architecture changes.

Historical documents are retained only when they provide useful provenance.
Superseded design drafts are kept under [`history/`](history/) rather than
presented as current guidance.
