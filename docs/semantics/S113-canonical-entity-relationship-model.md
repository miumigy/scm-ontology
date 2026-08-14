# S113 — Canonical Entity / Relationship Model

S113 is the consolidation boundary between the semantic contracts established in S101–S112 and a single canonical model that can be implemented, validated, mapped, and loaded into a graph.

## 1. Scope

S113 does not attempt to define the complete machine-readable ontology. It establishes the canonical concept inventory and relationship vocabulary that later schema work (S114+) must encode.

The model deliberately separates:

- **Primitive** — irreducible semantic building block.
- **Core** — stable SCM concept that composes primitives.
- **Derived** — computed or assessed concept whose meaning depends on other concepts.
- **Contextual** — reusable context/governance concept that qualifies core concepts.

It also records the dominant semantic world:

- **Physical** — things, resources, locations, inventory, and movement.
- **Information** — demand, orders, measurements, observations, and records.
- **Decision** — objectives, constraints, policies, plans, decisions, and actions.
- **Semantic** — concepts used to describe, qualify, identify, or explain the other worlds.

These are modeling dimensions, not four isolated ontologies.

## 2. Canonical entity policy

The canonical model uses an abstract `Entity` primitive for anything that can have identity in the SCM world. Domain concepts are promoted to named entities only when they have an independent identity, lifecycle, state, or graph role.

### Primitive

| Concept | Kind | World | Boundary |
|---|---|---|---|
| Entity | primitive | semantic | Canonical identifiable thing; not a source record |
| Event | primitive | semantic | Occurrence; not a state |
| State | primitive | semantic | Condition/configuration; not an occurrence |
| Observation | primitive | information | Assertion about what was observed; not automatically an inference |
| Time | primitive | semantic | Temporal semantics; an instant is not a Time entity |

### Core

| Concept | World | Notes |
|---|---|---|
| Actor | physical / decision | Participant capable of roles or decisions |
| Organization | physical / decision | Actor representing an organizational party |
| Location | physical | Geographic or logical place |
| Node | physical | Operational role in a supply-chain network |
| Product | physical | Intended output or sellable supply-chain item |
| Material | physical | Input/component used by transformation |
| Resource | physical | Capacity-bearing means used by operations |
| Inventory | physical | Stock position of an item at a context and time |
| Demand | information | Requirement or expected need for quantity/service |
| Order | information | Business request/transaction expressing demand or supply intent |
| Supply | physical / information | Availability or provision of item/resource/capacity |
| Capacity | physical | Available or usable capability over a scope and period |
| Flow | physical | Movement/transformation of supply-chain objects |
| Fulfillment | information / physical | Satisfaction of demand or order requirements |
| Plan | decision | Intended future configuration or action set |
| Schedule | decision | Time-positioned plan commitments or activities |
| Commitment | decision | Explicit promise or obligation |
| Objective | decision | Desired outcome or optimization direction |
| Constraint | decision | Boundary limiting feasible decisions/actions |
| Policy | decision | Governing decision rule or preference structure |
| Decision | decision | Selected course of action among alternatives |
| Action | physical / decision | Executed intervention intended to change the world |
| Outcome | semantic | Result attributable to an action/decision/context |
| Measurement | information | Measured value with unit/method/context |
| MetricDefinition | information | Meaning and calculation definition of a metric |
| MetricValue | information | Evaluated value of a MetricDefinition in a context |

## 3. Contextual concepts

The following are contextual concepts rather than additional domain primitives:

- Identity / Identifier / Alias
- Provenance / Source / Evidence
- Scenario / Counterfactual
- Validity / Effective Time / Transaction Time / Observation Time
- Unit of Measure
- Target / Threshold / Tolerance / Benchmark / Baseline
- Metric Scope / Period / Granularity / Aggregation
- Role / Responsibility / Authority
- Version

These concepts qualify other objects and must not be duplicated as vendor-specific entities in Core.

## 4. Derived concepts

Derived concepts are explicitly downstream of primary observations, states, events, definitions, or references.

Examples:

- KPI
- KPI Status
- KPI Score
- Performance Assessment
- Performance Attribution
- Variance
- Deviation
- Adherence
- Accuracy
- Bias
- Precision
- Inventory Turns
- Days of Supply
- Service Level
- Capacity Utilization
- Risk Score

A derived concept must identify the semantic inputs and calculation/assessment definition on which it depends. A derived metric must not be promoted into the primitive Core merely because it is operationally important.

## 5. Planned / actual / epistemic boundary

The canonical model preserves the following distinctions:

```text
Plan / Schedule / Commitment
        ≠
Execution / Actual

Observation / Measurement
        ≠
Estimate / Prediction / Inference

Scenario / Counterfactual
        ≠
Actual history

Recommendation
        ≠
Decision

Decision
        ≠
Action

Action
        ≠
Outcome
```

A source system may collapse these distinctions; canonical mapping must not.

## 6. Canonical relationship vocabulary

Relationships are first-class semantic contracts. A relationship is not an implementation-specific edge label.

### Structural

- `contains`
- `part_of`
- `located_at`

### Participation / responsibility

- `plays_role`
- `places`
- `receives`
- `executes`
- `decided_by`
- `owned_by`

### Flow / transformation

- `moves_through`
- `flows_to`
- `supplies`
- `consumes`
- `produces`
- `transforms`
- `fulfills`
- `allocated_to`
- `reserved_for`

### Planning / commitment / execution

- `planned_for`
- `scheduled_for`
- `committed_to`
- `executes`
- `results_in`

### Governance / decision

- `has_objective`
- `constrained_by`
- `governed_by`
- `considers`
- `selects`
- `recommends`

### Observation / measurement / derivation

- `observed_at`
- `measured_by`
- `derived_from`
- `evaluated_by`
- `supported_by`

### Causality / impact

- `causes`
- `affects`
- `depends_on`

These labels are intentionally lower-case canonical predicates. Vendor or source-system edge labels remain mapping/provenance data.

## 7. Relationship signatures

The initial signature set is intentionally small. Later milestones may add signatures only when a semantic gap is demonstrated.

| Predicate | Source | Target | Category |
|---|---|---|---|
| contains | Entity | Entity | structural |
| part_of | Entity | Entity | structural |
| located_at | Entity | Location | structural |
| plays_role | Actor | Entity | participation |
| places | Actor | Order | participation |
| receives | Actor | Entity | participation |
| executes | Actor | Action | participation |
| moves_through | Flow | Node | flow |
| flows_to | Flow | Node | flow |
| supplies | Actor | Supply | flow |
| consumes | Flow | Material | flow |
| produces | Flow | Product | transformation |
| transforms | Flow | Product | transformation |
| fulfills | Fulfillment | Demand | fulfillment |
| allocated_to | Supply | Demand | fulfillment |
| reserved_for | Supply | Demand | fulfillment |
| planned_for | Plan | Entity | planning |
| scheduled_for | Schedule | Entity | planning |
| committed_to | Commitment | Entity | commitment |
| results_in | Action | Outcome | lifecycle |
| has_objective | Decision | Objective | governance |
| constrained_by | Decision | Constraint | governance |
| governed_by | Decision | Policy | governance |
| considers | Decision | Entity | decision |
| selects | Decision | Entity | decision |
| observed_at | Observation | Entity | epistemic |
| measured_by | MetricValue | Measurement | measurement |
| derived_from | Entity | Entity | derivation |
| evaluated_by | Entity | MetricDefinition | evaluation |
| supported_by | Entity | Evidence | provenance |
| causes | Entity | Entity | causal |
| affects | Entity | Entity | causal |
| depends_on | Entity | Entity | dependency |

The same predicate may be used across multiple domain subtypes only when its meaning remains unchanged. If the meaning changes, define a distinct predicate rather than relying on overloaded labels.

## 8. Modeling rules

1. Do not create an entity merely because a source table has a row type.
2. Do not encode a relationship as an entity unless the relationship itself has identity/lifecycle or requires relationship-level state that cannot be represented as qualifiers.
3. Do not infer causality from `affects`, correlation, attribution, or temporal succession.
4. Do not use `actual` as a generic state that overwrites planned semantics.
5. Do not treat MetricDefinition, MetricValue, KPI, and PerformanceAssessment as interchangeable.
6. Preserve provenance and temporal qualification when mapping source data.
7. Keep source-specific identifiers outside canonical identity while retaining their mapping.
8. Keep derived metrics outside the primitive Core.
9. Prefer explicit relationship signatures over unrestricted `* -> *` edges.
10. The canonical model is a contract for mapping and graph reasoning, not a copy of an ERP or qualification framework.

## 9. S113 exit criteria

S113 is complete when:

- the canonical concept layers are explicit;
- physical, information, decision, and semantic dimensions are distinguishable;
- primitive/core/derived/contextual boundaries are machine-readable;
- the initial relationship vocabulary has explicit signatures;
- planned/actual and epistemic distinctions are protected;
- the model can be validated independently of YAML source-system schemas.

Machine-readable serialization and attribute/value semantics are intentionally deferred to S114–S116.
