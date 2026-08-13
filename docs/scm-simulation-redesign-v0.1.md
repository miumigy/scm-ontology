# SCM Simulation Redesign v0.1

Status: Design baseline
Date: 2026-08-14

## 1. Purpose

This document redefines the future SCM simulation architecture around the SCM Ontology rather than around the legacy `scsim` implementation.

The goal is to define a framework-independent simulation model in which SCM state changes are caused by events, constraints, policies, and decisions, and whose outcomes can be represented back in the canonical SCM Ontology and SCM Graph.

The intended loop is:

```text
Enterprise / ERP / WMS / TMS / Planning / Simulation
                         |
                         v
                  SCM Ontology
                         |
                         v
                     SCM Graph
                         |
                 +-------+-------+
                 |               |
              Reasoning       Scenario
                 |               |
                 +-------+-------+
                         |
                         v
                    Simulation
                         |
                         v
                 KPI / Risk / Impact
                         |
                         v
                     Decision
```

Simulation is a consumer and producer of canonical SCM state, not the owner of the semantic model.

## 2. Relationship to legacy scsim

The existing `miumigy/scsim` repository is a useful proof-of-concept and educational simulator. Its current README describes a self-contained browser application based on stock points and flows, PSI conservation, cost visualization, configurable demand/lead time/capacity/cost, and turn-based scenario simulation. Its main branch has not materially evolved since June 2025.

Legacy strengths to preserve:

- PSI and inventory-flow consistency
- transparent business logic
- scenario experimentation
- browser/mobile accessibility
- cost and KPI visibility
- deterministic, inspectable examples

Legacy assumptions to remove from the new core:

- stock-point/flow as the universal simulation abstraction
- single fixed network topology
- simulation state owned by UI configuration
- turn advancement as the primary temporal abstraction
- simulator-specific entities duplicating the Canonical Ontology
- coupling of simulation semantics to one visualization or browser runtime

## 3. Core principle

The fundamental simulation unit is:

```text
State + Event + Transition + Decision + Constraint
```

rather than merely:

```text
Flow Unit + Stock Point
```

A simulation advances when an event occurs or a decision is applied, producing a validated state transition.

```text
State(t)
   |
   | Event / Decision under Constraints
   v
Transition
   |
   v
State(t+dt)
   |
   +--> KPI change
   +--> Risk change
   +--> downstream Events
```

## 4. Canonical simulation concepts

### Scenario

A Scenario defines a controlled counterfactual experiment. It contains a baseline state reference, assumptions, parameters, injected events, alternative decisions, policies, simulation horizon, execution settings, and a random seed when stochastic behavior is enabled.

Examples: Supplier A lead time +7 days; Supplier A capacity -30%; Factory F-001 capacity +20%; Demand +15%; dual sourcing Supplier A / Supplier B.

### State

State is the time-indexed condition of the modeled supply chain. It may contain entity attributes, inventory positions, order/shipment/production/site/supplier states, capacity availability, demand backlog, planned and inbound supply, cost/cash measures, active risks, and active constraints.

State must use canonical entity identity. The simulator must not create a second identity system for Product, Site, Material, Supplier, etc.

### Event

An Event represents an occurrence that changes or can change SCM state. Examples include `SUPPLIER_DELAY`, `MATERIAL_SHORTAGE`, `PRODUCTION_START`, `PRODUCTION_COMPLETE`, `SHIPMENT_DEPARTED`, `SHIPMENT_DELAY`, `DEMAND_ARRIVAL`, `STOCKOUT`, and `CAPACITY_DOWN`.

Events may be observed historical events, externally injected scenario events, or internally generated simulation events.

### State Transition

A transition is an inspectable transformation:

```text
(previous_state, event, decision, constraints, policy)
                 -> next_state
```

A transition should produce an audit record containing the event id, affected entity ids, changed attributes, before/after values, constraint checks, generated downstream events, and KPI deltas where applicable.

### Constraint

Constraints limit feasible transitions or decisions. Canonical categories include `CAPACITY`, `MATERIAL`, `INVENTORY`, `LEAD_TIME`, `MOQ`, `LOT_SIZE`, `STORAGE`, `TRANSPORT`, `SUPPLIER`, `QUALITY`, `REGULATORY`, and `BUDGET`.

Constraints must be evaluated explicitly rather than hidden inside flow calculations.

### Policy

Policies describe operating or decision rules, including `SAFETY_STOCK`, `REORDER_POINT`, `MIN_MAX`, `BASE_STOCK`, `SOURCING`, and `ALLOCATION`.

Policies should be replaceable without changing the underlying state model.

### Decision

A Decision is an intentional choice among feasible options. Examples include `SUPPLIER_SELECTION`, `PURCHASE_PLAN`, `PRODUCTION_PLAN`, `PRODUCTION_SCHEDULE`, `REPLENISHMENT`, `EXPEDITE`, `DEFER`, `TRANSPORT_MODE`, and `SUPPLY_ALLOCATION`.

A decision records its options, selected option, objectives, applicable constraints, and resulting state transition(s).

## 5. Time model

The runtime should support both discrete-event progression and fixed time-step progression where useful for planning or visualization. The semantic model is event-oriented; a fixed time step is an execution strategy, not a semantic requirement.

Temporal facts should be representable with event time, effective time, `validFrom`, `validTo` where appropriate, duration, lead time, and simulation clock.

Simulation output must be reproducible from the same baseline state, scenario, configuration, and random seed.

## 6. Causal model

The simulation must preserve the causal chain already established in the SCM Ontology:

```text
Constraint -> Decision -> Execution -> Event
                                   |
                                 CAUSES
                                   v
                            Downstream Event
                                   |
                                IMPACTS
                                   v
                                KPI / Risk
```

Example:

```text
Supplier lead time +7d
        |
        v
SUPPLIER_DELAY
        |
      CAUSES
        v
MATERIAL_SHORTAGE
        |
      CAUSES
        v
PRODUCTION_DELAY
        |
      CAUSES
        v
SHIPMENT_DELAY
        |
      IMPACTS
        +--------> Customer Service Risk
        +--------> ON_TIME_DELIVERY
```

The simulator should preserve the causal path that produced a KPI, not merely calculate the final KPI.

## 7. Simulation output

Simulation output is a first-class semantic artifact.

Minimum `SimulationRun` metadata:

- run id
- scenario id
- baseline state id
- engine version
- ontology version
- random seed
- simulation start/end time
- events processed
- decisions applied
- state snapshots or deltas
- KPI outcomes
- risk outcomes
- causal impacts

Runs must be comparable.

## 8. Determinism and stochastic simulation

The core engine is deterministic by default. Stochastic execution uses an explicit random seed; distributions and parameters are part of the scenario; seed and configuration are persisted; identical inputs reproduce identical outputs.

Monte Carlo execution should be a wrapper around the deterministic run engine:

```text
Scenario
   |
   +--> seed 1 --> deterministic run
   +--> seed 2 --> deterministic run
   +--> seed 3 --> deterministic run
              |
              v
        aggregated outcomes
```

## 9. Optimization interface

Optimization is not part of the minimum simulation kernel. The kernel exposes an interface so an optimizer can search over canonical decisions or policy parameters:

```text
Decision Space -> Simulation Run -> Objective / Constraints -> Candidate Score
```

Candidate decisions remain canonical `Decision` objects. Optimization must not introduce a second decision representation.

Potential objectives include `MAXIMIZE_SERVICE`, `MINIMIZE_TOTAL_COST`, `MINIMIZE_INVENTORY`, `MINIMIZE_LEAD_TIME`, `MAXIMIZE_MARGIN`, and `BALANCE_SERVICE_COST_CASH`.

## 10. KPI and risk evaluation

KPI calculations consume canonical state and event history. Risk is derived from current state, constraint exposure, event propagation, and KPI impact; it is not merely a static label attached to an entity.

## 11. Ontology integration boundary

The simulation runtime has an explicit adapter boundary:

```text
SCM Ontology
     ^
     | canonical state / events / decisions
     |
Simulation Adapter
     |
Simulation Runtime
```

The adapter translates canonical entities into runtime state, runtime changes into canonical state/event records, preserves canonical ids and relationship semantics, validates state before and after transitions, and produces idempotent graph-ingestion payloads.

The simulation engine must not mutate the ontology definition itself.

## 12. Graph integration

For what-if analysis, a scenario-specific graph/state projection is preferred over destructive mutation of the baseline graph.

```text
Baseline Graph -> Scenario Event -> Simulation -> State/Event deltas -> Graph projection -> Impact Analysis -> KPI/Risk
```

Neo4j is a graph implementation choice, not a simulation-kernel requirement.

## 13. Example: supplier delay

Baseline:

```text
Demand = 100
Available = 60
Inbound = 20
Gap = 100 - 60 - 20 = 20
```

Scenario: `Supplier A lead time +7 days`.

Expected causal progression:

```text
SUPPLIER_DELAY
      |
      v
Inbound timing changes
      |
      v
Available supply window changes
      |
      v
Supply Gap increases
      |
      v
Production constraint / delay
      |
      v
Shipment delay
      |
      v
ON_TIME_DELIVERY risk
```

The exact propagation depends on scenario state and constraints; the engine must not hard-code this chain as a universal rule.

## 14. Runtime architecture

```text
+--------------------------------------------------+
|                 Scenario Layer                   |
| assumptions / events / decisions / parameters    |
+--------------------------------------------------+
                       |
                       v
+--------------------------------------------------+
|               Simulation Kernel                  |
| clock / event queue / transitions / constraints  |
+--------------------------------------------------+
                       |
                       v
+--------------------------------------------------+
|                State Store                       |
| canonical entity state + simulation metadata     |
+--------------------------------------------------+
                       |
             +---------+---------+
             |                   |
             v                   v
      KPI / Risk Engine     Event/Causal Log
             |                   |
             +---------+---------+
                       |
                       v
+--------------------------------------------------+
|          Ontology / Graph Adapter                |
+--------------------------------------------------+
```

The UI is outside the core runtime.

## 15. Conceptual runtime contract

The first implementation should expose a small contract similar to:

```text
load_baseline(ontology_state)
create_scenario(baseline, assumptions, events, decisions)
run(scenario) -> SimulationRun
apply_event(state, event) -> Transition
apply_decision(state, decision) -> Transition
validate_state(state) -> ValidationResult
calculate_kpis(run) -> KPISet
export_canonical(run) -> OntologyPayload
```

This is a conceptual contract, not yet a commitment to a programming language or package structure.

## 16. Testing strategy

### Level 1: semantic invariants

- canonical ids remain stable
- state transitions preserve entity identity
- invalid transitions are rejected
- constraints are enforced
- event causality is recorded

### Level 2: conservation / accounting

- inventory conservation
- material balance
- shipment quantity consistency
- cost/cash consistency where modeled

### Level 3: scenario regression

- supplier delay
- demand increase
- capacity reduction
- stockout
- dual sourcing

### Level 4: reproducibility

- same seed + same inputs = same result
- different seeds can produce different stochastic outcomes

### Level 5: integration

- ontology -> simulation
- simulation -> ontology
- simulation -> graph
- graph impact analysis -> KPI/risk

## 17. Non-goals for v0.1

The redesign does not attempt to immediately provide enterprise-grade real-time planning, a full ERP replacement, a universal optimization solver, detailed physical manufacturing simulation, perfect stochastic modeling of every SCM process, proprietary APICS/ASCM content reproduction, a mandatory Neo4j dependency inside the simulation kernel, or a mandatory browser UI.

## 18. Implementation roadmap

### S0 — Specification

This document and canonical simulation contracts.

### S1 — Minimal deterministic kernel

State, Event, Transition, Constraint, Scenario, SimulationRun.

### S2 — Automotive vertical scenario

Customer -> Demand -> Product -> ProductLocation -> Inventory -> BOM -> Material -> Supplier -> Factory -> Warehouse -> Lane -> Shipment.

### S3 — Ontology adapter

Canonical YAML/graph state -> simulation runtime -> canonical event/state deltas.

### S4 — Causal simulation

Generate downstream events and preserve `CAUSES` / `IMPACTS` semantics.

### S5 — Scenario comparison

Baseline vs alternatives, KPI/risk deltas, reproducible run metadata.

### S6 — Stochastic / Monte Carlo wrapper

Seeded stochastic execution and outcome distributions.

### S7 — Decision simulation

Decision options, objective functions, constrained candidate evaluation.

### S8 — scsim successor

Only after the semantic/runtime contract stabilizes, implement the next-generation user-facing simulator. The existing `scsim` becomes a reference/legacy implementation rather than a dependency of the ontology.

### S9 — AI reasoning interface

Natural-language what-if question -> Scenario -> Simulation -> Impact Analysis -> Decision recommendation.

## 19. Architectural invariants

1. SCM Ontology owns canonical semantics; Simulation does not.
2. Canonical entity identity is stable and idempotent.
3. Simulation state is time-indexed.
4. State changes are explainable through Events, Decisions, Constraints, and Policies.
5. Causal relationships are preserved, not reduced to final KPI values.
6. Simulation outputs are machine-readable and graph-compatible.
7. The deterministic kernel is reproducible.
8. Stochastic behavior is explicitly seeded and parameterized.
9. Optimization consumes and produces canonical Decisions.
10. UI and visualization are replaceable implementation layers.
11. Neo4j is a graph implementation choice, not a simulation-kernel requirement.
12. External frameworks such as APICS/SCOR remain mapping sources, not ontology owners.

## 20. Decision: what happens to scsim?

The existing `scsim` should not be incrementally forced to implement this architecture.

```text
scsim v1
  = legacy educational / reference simulator

SCM Simulation Specification
  = canonical design authority

scsim v2 / scm-sim
  = future implementation of the specification
```

The existing implementation can contribute tested business examples, UI ideas, conservation rules, and scenario fixtures. Its internal model should not become the semantic contract of the SCM Ontology.

## 21. Long-term vision: Supply Chain Decision Twin

```text
Reality
   |
   v
SCM Ontology
   |
   v
SCM Graph
   |
   +-------------------+
   |                   |
   v                   v
Current State       Scenario
                       |
                       v
                  Simulation
                       |
              +--------+--------+
              v                 v
            Impact             KPI
              |                 |
              +--------+--------+
                       v
                    Decision
                       |
                       v
                 SCM Execution
```

The target is a Supply Chain Decision Twin: a semantic, causal, simulation-capable model that can answer not only "what is happening?" but also "what happens if we change this?" and eventually "which decision should we take?".
