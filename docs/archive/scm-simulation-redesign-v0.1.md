# SCM Simulation Redesign v0.1

> Historical design baseline from 2026-08-14. Archived after M8 completion.

This document defined the pre-M8 direction for an SCM Ontology-centered simulation architecture. It treated simulation as a consumer/producer of canonical SCM state rather than the owner of ontology semantics.

## Historical architecture

```text
Enterprise / ERP / WMS / TMS / Planning
                 |
                 v
           SCM Ontology
                 |
                 v
             SCM Graph
              /     \
        Reasoning   Scenario
              \     /
               Simulation
                   |
             KPI / Risk / Impact
                   |
                Decision
```

The baseline introduced the concepts of Scenario, State, Event, State Transition, Constraint, Policy, Decision, deterministic execution, causal propagation, simulation outputs, graph integration, and a future Supply Chain Decision Twin.

## Historical implementation roadmap

S1 Minimal deterministic kernel → S2 automotive scenario → S3 ontology adapter → S4 causal simulation → S5 scenario comparison → S6 stochastic/Monte Carlo → S7 decision simulation → S8 scsim successor → S9 AI reasoning interface.

## Current status

M8 has superseded this design baseline with governed canonical graph, projection, consistency, operational-readiness, and acceptance contracts. For current guidance, use the repository README, `docs/architecture/current-architecture.md`, `docs/history/post-m8-roadmap.md`, and the M8 milestone acceptance documentation.

The complete original text remains recoverable from Git history.
