# Operations — SCM OS Reference Runtime

This directory documents the **governed SCM OS reference runtime**: the
deterministic decision loop, its reasoning providers, bounded execution,
governance, and the reference SCM applications built on top of them.

These are the current-product Operation contracts of **SCM Ontology v0.1.0 /
SCM OS Reference v0.1.0**. They implement, execute, and operate the semantic
model under explicit governance. They do **not** define new canonical semantics;
the semantics live under [`docs/semantics/`](../semantics/).

## Decision runtime

- [`decision-runtime.md`](decision-runtime.md) — the deterministic, side-effect-free governed decision runtime
- [`rule-reasoning-provider.md`](rule-reasoning-provider.md) — deterministic rule-based reasoning provider
- [`llm-reasoning-provider.md`](llm-reasoning-provider.md) — injected, transport-neutral LLM reasoning provider

## Execution & governance

- [`execution-runtime.md`](execution-runtime.md) — in-memory, side-effect-free execution runtime
- [`governed-audit.md`](governed-audit.md) — content-addressed audit trail & deterministic replay
- [`command-lifecycle.md`](command-lifecycle.md) — immutable, append-only command lifecycle
- [`authorization-governance.md`](authorization-governance.md) — fail-closed authorization, approval & override

## Applications

- [`replenishment-application.md`](replenishment-application.md) — on-hand inventory -> replenishment decision
- [`procurement-application.md`](procurement-application.md) — demand/supply shortage -> procurement decision
- [`production-application.md`](production-application.md) — requirement vs capacity -> production decision
- [`distribution-application.md`](distribution-application.md) — shipment vs transport capacity -> distribution decision
- [`governed-simulation.md`](governed-simulation.md) — multi-period, multi-decision governed simulation
- [`optimized-planning.md`](optimized-planning.md) — deterministic multi-period replenishment optimization
- [`optimized-app-planning.md`](optimized-app-planning.md) — deterministic optimization across procure / produce / distribute
- [`operational-workflow.md`](operational-workflow.md) — operational workflow & reporting slice

## Reasoning & query contracts

- [`constraint-reasoning.md`](constraint-reasoning.md) — constraint-aware semantic path reasoning
- [`temporal-semantic-query.md`](temporal-semantic-query.md) — governed read-only temporal semantic query
- [`scenario-overlay.md`](scenario-overlay.md) — immutable what-if scenario overlay
- [`evidence-aware-traversal.md`](evidence-aware-traversal.md) — evidence-aware temporal traversal
- [`evidence-aware-projection.md`](evidence-aware-projection.md) — evidence-aware projection
- [`projection-freshness-invalidation.md`](projection-freshness-invalidation.md) — projection freshness & invalidation runtime
- [`governed-projection-query.md`](governed-projection-query.md) — governed projection query surface

## Business-question slices

- [`inventory-position.md`](inventory-position.md) — canonical inventory position
- [`demand-supply-gap.md`](demand-supply-gap.md) — canonical demand / supply gap
- [`supplier-delay-impact.md`](supplier-delay-impact.md) — canonical supplier delay impact
- [`multi-hop-supply-risk.md`](multi-hop-supply-risk.md) — canonical multi-hop supply risk
- [`capacity-constraint.md`](capacity-constraint.md) — canonical capacity constraint
- [`network-disruption-propagation.md`](network-disruption-propagation.md) — canonical network disruption propagation
- [`plan-actual-commitment-reconciliation.md`](plan-actual-commitment-reconciliation.md) — canonical plan/actual/commitment reconciliation
