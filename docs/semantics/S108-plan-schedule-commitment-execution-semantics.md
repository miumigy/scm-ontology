# S108 — Plan, Schedule, Commitment & Execution Semantics

S108 defines the semantic boundary between Plan, Schedule, Commitment, Planned Action, Execution, Actual Action, and Outcome.

## Canonical decision

A Plan describes intended future behavior. A Schedule assigns temporal and resource structure to intended work. A Commitment represents an accepted obligation or promise. Execution represents what was actually performed.

```text
Context
  ↓
Plan
  ↓
Schedule
  ↓
Commitment
  ↓
Planned Action
  ↓
Execution
  ↓
Actual Action
  ↓
Outcome
```

These artifacts must remain distinguishable because operational reality can diverge from intent.

## Plan

A Plan is an intentional representation of a proposed or selected future course of operations.

Examples:

```text
production plan
procurement plan
inventory plan
transport plan
network plan
replenishment plan
```

A Plan may contain Decisions, intended Actions, assumptions, constraints, objectives, and alternatives.

## Plan versus Decision

A Decision selects an option or course of action.

A Plan organizes one or more intended Decisions and Actions into a coherent future operating structure.

```text
Decision
  ↓
Plan
  ├─ intended Action A1
  ├─ intended Action A2
  └─ intended Action A3
```

A Plan may therefore contain multiple Decisions, while a Decision need not constitute a complete Plan.

## Plan versus Forecast

A Forecast predicts what is expected to happen.

A Plan specifies what is intended to happen.

```text
Forecast: demand expected = 1,000
Plan: produce = 900
```

Forecast and Plan may influence each other but must not be conflated.

## Plan versus Scenario

A Scenario represents a hypothetical context or alternative world model.

A Plan represents intended operational behavior within an applicable context.

```text
Scenario A
  ↓
Plan A
```

A scenario may contain candidate plans without making them actual operational Plans.

## Plan status

A Plan may have lifecycle states such as:

```text
draft
proposed
approved
released
active
superseded
cancelled
completed
```

The exact vocabulary is domain-specific.

## Plan version

Plans may be revised over time.

```text
Plan P1 v1
   ↓ revision
Plan P1 v2
```

Historical versions should remain reconstructable where decisions or commitments depended on them.

## Plan revision versus Plan replacement

A revision changes the intended operating structure while preserving semantic continuity where appropriate.

A replacement may establish a new Plan identity.

The distinction should be explicit when historical traceability matters.

## Schedule

A Schedule assigns temporal ordering, timing, duration, or resource placement to planned work.

Examples:

```text
production schedule
shipment schedule
maintenance schedule
warehouse labor schedule
```

A Schedule may operationalize a Plan.

```text
Plan
 ↓
Schedule
```

## Schedule versus Plan

```text
Plan
  = intended operating structure

Schedule
  = temporal/resource realization of intended work
```

A Plan may exist without a detailed Schedule.

A Schedule may be regenerated while the underlying Plan remains semantically continuous.

## Scheduled time

Scheduled Time describes when an Action or Activity is intended to occur according to a Schedule.

It is not the same as Actual Time.

```text
scheduled_start = 10:00
actual_start    = 10:17
```

S106 governs the temporal dimensions.

## Commitment

A Commitment is an accepted obligation, promise, reservation, allocation, or declared intention that creates an expectation between relevant parties or within a governed process.

Examples:

```text
supplier commits to deliver 1,000 units
carrier commits to pickup at 10:00
factory commits to produce 500 units
planner commits inventory to Order O1
```

Commitment semantics may be internal or inter-organizational.

## Commitment versus Plan

A Plan describes intended behavior.

A Commitment establishes an accepted obligation or expectation.

```text
Plan:
produce 1,000 units

Commitment:
Supplier agrees to deliver 1,000 units by Friday
```

A Plan does not automatically create a Commitment.

## Commitment authority

A Commitment may require an authorized Actor.

```text
Actor
  ↓ authority
Commitment
```

A forecast, suggestion, or draft plan does not become a Commitment merely because it is system-generated.

## Commitment scope

A Commitment may specify:

```text
committing Actor
counterparty
object
quantity
quality
location
validity period
due time
conditions
exceptions
```

The applicable dimensions depend on the domain.

## Commitment status

A Commitment may have states such as:

```text
proposed
accepted
confirmed
active
partially_fulfilled
fulfilled
breached
cancelled
expired
```

The exact lifecycle is domain-specific.

## Commitment versus Obligation

An Obligation describes a required behavior under a governing context.

A Commitment represents an accepted promise or declared obligation in a specific operational context.

```text
Policy / Contract
      ↓
Obligation
      ↓
Commitment
```

A Commitment may operationalize an Obligation but is not necessarily equivalent to it.

## Commitment versus Authorization

Authorization determines whether an Actor is permitted to perform an Action.

Commitment determines whether an accepted promise or obligation exists.

```text
Authorization
  = may act

Commitment
  = has committed
```

These should not be conflated.

## Planned Action

A Planned Action is an intended execution step contained in or derived from a Plan or Decision.

```text
Decision
  ↓
Planned Action
```

It represents intent rather than completed execution.

## Execution

Execution is the operational process by which a Planned Action is attempted or performed.

```text
Planned Action
      ↓
Execution
```

Execution may begin, pause, fail, partially complete, or complete.

## Actual Action

An Actual Action represents what was actually performed or initiated in operational reality.

```text
Planned Action
      ↓
Execution
      ↓
Actual Action
```

The Actual Action may differ from the Planned Action.

## Planned versus Actual

The ontology must preserve divergence between intent and reality.

```text
Plan:
Route A

Actual:
Route B
```

The Plan should not be rewritten to Route B merely because Route B was executed.

## Deviation

A Deviation describes a material difference between intended and actual behavior.

Examples:

```text
planned quantity = 1,000
actual quantity = 800

planned departure = 10:00
actual departure = 10:42

planned route = A
actual route = B
```

Deviation is an analytical relation, not necessarily an Event itself.

## Variance

Variance describes a measured difference between planned, scheduled, committed, forecast, or target values and actual results.

```text
planned = 1,000
actual  = 800
variance = -200
```

Variance semantics should identify the reference basis explicitly.

## Plan adherence

Plan Adherence evaluates how closely execution followed a Plan.

```text
Plan
 ↓ compare
Actual Execution
 ↓
adherence assessment
```

Adherence is distinct from Plan validity or quality.

## Schedule adherence

Schedule Adherence evaluates actual timing against Scheduled Time.

```text
scheduled = 10:00
actual    = 10:17
```

This may support lateness or earliness metrics.

## Commitment fulfillment

Commitment Fulfillment evaluates whether an accepted Commitment was satisfied.

```text
Commitment:
1,000 units by Friday

Actual:
800 units by Friday

→ partially fulfilled
```

Fulfillment is an assessment and should not overwrite the original Commitment.

## Commitment breach

A Commitment Breach represents a material failure to satisfy a Commitment according to applicable semantics.

A breach may require evaluation of:

```text
scope
validity
exceptions
waivers
force majeure
measurement basis
```

A variance does not automatically constitute a breach.

## Exception and commitment

An authorized Exception may modify how a Commitment is interpreted or fulfilled.

```text
Commitment
   ↓
Exception / Waiver
   ↓
revised fulfillment condition
```

The original Commitment remains historically identifiable.

## Plan approval

Plan Approval is a Decision or authorization that makes a Plan applicable for execution.

```text
Draft Plan
   ↓ approval
Approved Plan
```

Approval does not guarantee execution.

## Plan release

Plan Release indicates that a Plan or part of it has been made available for operational execution.

```text
Approved Plan
   ↓ release
Executable Plan
```

Release is distinct from approval.

## Plan freeze

A Plan Freeze establishes a period or scope in which changes are restricted or controlled.

```text
Frozen horizon
  ↓
change requires exception / authority
```

Freeze semantics are contextual and should not be treated as universal immutability.

## Planning horizon

A Planning Horizon defines the temporal range considered by a Plan or planning process.

```text
past | current | planning horizon | beyond horizon
```

Planning Horizon is contextual and does not necessarily define the Plan's validity period.

## Firm horizon

A Firm Horizon identifies a portion of the planning horizon in which changes are restricted, costly, or require explicit approval.

Firmness is a governance or planning property, not a universal temporal primitive.

## Frozen versus committed

```text
Frozen
  = changes are restricted

Committed
  = accepted obligation / expectation exists
```

A Plan may be frozen without creating an external Commitment, and a Commitment may exist even when the internal Plan remains changeable within agreed boundaries.

## Allocation

Allocation assigns a resource, capacity, inventory quantity, or other limited object to a Candidate, Order, Plan, or Commitment.

```text
Inventory I1
  ↓ allocation
Order O1
```

Allocation does not necessarily imply physical movement or consumption.

## Reservation

Reservation represents a protected or held allocation for intended future use.

```text
Available
  ↓ reservation
Reserved
```

Reservation is distinct from actual consumption.

## Promise

A Promise is a commitment-oriented representation of expected delivery, service, capacity, or performance.

```text
Promise
  ↓
Commitment
```

The exact relationship depends on the business process.

## Confirmation

Confirmation indicates that an intended or proposed Plan, Schedule, Order, or Commitment has been explicitly accepted or acknowledged.

Confirmation should not be treated as proof of actual execution.

## Execution status

Execution may be:

```text
not_started
in_progress
partially_completed
completed
failed
cancelled
aborted
```

Execution status belongs to execution semantics rather than the original Plan.

## Partial execution

A Planned Action may be partially executed.

```text
planned = 1,000
actual = 600
```

The remaining 400 should remain semantically distinguishable from the 600 already executed.

## Replanning

Replanning creates or revises future intent based on new information, constraints, or outcomes.

```text
Plan v1
  ↓ new Observation / Event
Plan v2
```

Replanning must not rewrite the historical Plan v1.

## Rescheduling

Rescheduling changes the temporal arrangement of intended work while preserving relevant semantic continuity.

```text
scheduled = 10:00
   ↓ reschedule
scheduled = 14:00
```

The reason, authority, and validity context may be retained where material.

## Cancellation

Cancellation terminates or invalidates future execution of a Plan, Schedule, Commitment, or Action according to its semantics.

Cancellation is not equivalent to historical deletion.

## Supersession

A Plan or Schedule may be superseded by a later version.

```text
P1
 ↓ superseded-by
P2
```

P1 remains available for historical reconstruction where required.

## Execution feedback

Execution produces Events, Observations, and Outcomes that can feed the next planning cycle.

```text
Plan
 ↓
Execution
 ↓
Outcome / Observation
 ↓
Evaluation
 ↓
Replan
```

This connects S108 to the closed-loop semantics of S100–S107.

## Plan and Decision provenance

A Plan should be traceable to the Decisions, Policies, Constraints, Objectives, and Evidence that materially informed it where auditability matters.

```text
Evidence
  ↓
Evaluation
  ↓
Decision
  ↓
Plan
```

S104 provides provenance and lineage semantics.

## Temporal semantics

S106 governs temporal distinctions relevant to Plans and Schedules.

For example:

```text
plan_created_at
plan_valid_from
scheduled_start
scheduled_end
actual_start
actual_end
```

These timestamps must not be collapsed into a single creation timestamp.

## Identity semantics

S105 governs identity of Plans, Orders, Activities, Assets, and other relevant Entities.

A revised Plan may either:

```text
retain identity with a new version
```

or:

```text
create a successor Plan
```

according to explicit governance semantics.

## Epistemic semantics

A Plan is an intention, not a guarantee of future reality.

Therefore:

```text
Plan
  ≠ Forecast
  ≠ Actual Event
  ≠ Outcome
```

A plan may also carry assumptions or confidence, but these do not turn intent into fact.

## Scenario planning

Scenario Plans are hypothetical plans evaluated under Scenario assumptions.

```text
Scenario A
  ↓
Plan A
  ↓
Projected Outcome
```

They must remain distinct from the operational Plan adopted for actual execution.

## Counterfactual planning

Counterfactual Plans describe what would have been done under an alternative condition.

They must not be represented as historical Plans that were actually released or executed.

## Decision and Plan relationship

A Decision may:

```text
approve a Plan
select a Plan
modify a Plan
cancel a Plan
request replanning
```

The relationship should remain explicit.

## Action and Plan relationship

A Plan may contain many Planned Actions.

```text
Plan P1
 ├─ Planned Action A1
 ├─ Planned Action A2
 └─ Planned Action A3
```

Actual Actions may later diverge from these Planned Actions.

## Outcome and Plan relationship

An Outcome may be evaluated against a Plan without implying that the Plan caused every observed consequence.

```text
Plan
 ↓ compare
Outcome
 ↓
Plan Performance Assessment
```

Causal claims remain governed by S101.

## No automatic commitment from plan

```text
Plan
  ≠ automatically
Commitment
```

A Commitment requires the applicable acceptance, authority, or governance semantics.

## No automatic execution from schedule

```text
Schedule
  ≠ automatically
Actual Action
```

A Schedule is intended timing, not evidence that work occurred.

## No retroactive plan mutation

Actual execution must not overwrite the historical Plan or Schedule.

```text
Plan v1
Schedule v1
   ↓
Actual execution
   ↓
Deviation
```

This is essential for measuring planning quality and operational adherence.

## No universal lifecycle

S108 does not mandate one universal Plan, Schedule, Commitment, or Execution lifecycle.

Different SCM domains may use different states and transitions.

## No mandatory planning fields

S108 does not require every Plan to contain:

```text
plan_id
version
start_time
end_time
owner
status
commitments
```

These are context-dependent semantics.

## Non-goals

S108 does not define a universal APS system, MRP algorithm, scheduling solver, project-management workflow, contract-management system, event-sourcing architecture, or execution engine.
