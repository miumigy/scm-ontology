# S106 — Temporal, State & Event Semantics

S106 defines how SCM Ontology represents events, states, state transitions, temporal intervals, and the different meanings of time required to reconstruct supply-chain reality and decisions.

## Canonical decision

Event, State, and State Transition are distinct semantic concepts.

```text
Event
  ↓ changes / informs
State
  ↓
State Transition
```

Time is also multidimensional.

```text
Effective Time
Transaction Time
Observation Time
Knowledge Time
Processing Time
```

These timestamps must not be silently collapsed into one universal `timestamp` when their distinctions affect meaning.

## Event

An Event is something that occurs, happens, or is recognized as occurring at a point or interval in time.

Examples:

```text
Order Created
Shipment Departed
Truck Arrived
Production Started
Production Completed
Inventory Counted
Delivery Confirmed
```

An Event is not the same as the persistent State that exists before or after it.

## State

A State describes a condition of an Entity, process, or system during a temporal interval.

Examples:

```text
Order.status = confirmed
Shipment.status = in_transit
Inventory.position = 512
Factory.status = operating
```

A State may persist while no Event occurs.

## State Transition

A State Transition represents a change from one State to another.

```text
confirmed
    ↓
allocated
```

The transition may be triggered by an Event, a Decision, an Action, an external condition, or an automated process.

## Event versus State

```text
Event
  = something happened

State
  = condition that holds
```

For example:

```text
Shipment departed at 10:42
  = Event

Shipment status = in_transit
  = State
```

The Event may explain why the State changed, but they are not interchangeable.

## Event versus Observation

An Event is a domain occurrence.

An Observation is an information representation of what is observed or recorded about reality.

```text
Real-world Event
      ↓
Observation / Record
```

The Event may occur even if it is not immediately observed or recorded.

## Event identity

An Event may have its own identity where it is necessary to distinguish one occurrence from another.

```text
ShipmentDeparture E1
  subject = Shipment S1
  occurred_at = T1
```

The identity of an Event should not be inferred solely from its associated Entity.

## Event time

An Event may have:

```text
occurred_at
started_at
ended_at
```

A point event may use a single temporal instant. A process or activity may require an interval.

## Temporal interval

An interval represents a period during which a State, Activity, or other temporal condition applies.

```text
[T1, T2)
```

The ontology should preserve boundary semantics where they matter.

## Open intervals

An interval may have an unknown or unbounded boundary.

```text
[T1, ∞)
(-∞, T2)
```

An open interval must not be converted into an arbitrary finite timestamp.

## Valid Time / Effective Time

Valid Time or Effective Time describes when a fact, state, relationship, or value is true or applicable in the modeled domain.

```text
Price = 100
valid_from = Aug 1
valid_to   = Aug 31
```

Effective Time is about the domain reality, not necessarily when the information was entered into a system.

## Transaction Time

Transaction Time describes when a system recorded, accepted, or stored an information state.

```text
occurred_at   = Aug 10 10:42
recorded_at   = Aug 11 08:15
```

The domain event occurred before the system transaction was recorded.

## Observation Time

Observation Time describes when an observation was made or obtained.

```text
sensor_observed_at = T1
```

Observation Time may differ from both Event Time and Transaction Time.

## Knowledge Time

Knowledge Time describes when an actor or system had access to information or when an assertion became knowable under the relevant context.

S103 defines its epistemic importance; S106 provides the temporal semantics needed to represent it.

```text
Event Time
    ≠ Observation Time
    ≠ Knowledge Time
    ≠ Transaction Time
```

## Processing Time

Processing Time describes when a system processed an artifact or event.

```text
occurred_at  = 10:42
received_at  = 10:45
processed_at = 10:46
```

Processing latency can therefore be represented without changing the event's occurrence time.

## Published Time

Published Time describes when information became available to downstream consumers or systems.

It may differ from transaction, observation, or event time.

## Recorded Time

Recorded Time describes when a record representing a fact or event was created or persisted.

It is implementation-dependent and should not automatically be treated as the event occurrence time.

## Time of Decision

Decision Time describes when a Decision was made.

This is critical for reconstructing the information state available to the decision maker.

```text
Decision D1
  decided_at = T1
```

## Time of Action

Action Time describes when an Action was executed or initiated.

```text
Decision Time
    ↓
Action Time
```

These may differ due to approval, scheduling, or execution delay.

## Time of Outcome

Outcome Time describes when the relevant consequence or result occurred or became effective.

```text
Action at T1
   ↓
Outcome at T2
```

Outcome Time should not automatically equal observation time.

## Temporal ordering

The ontology should permit temporal relationships such as:

```text
before
meets
overlaps
during
starts
finishes
equals
```

The exact interval algebra may be implemented using an appropriate temporal model.

## Causal ordering versus temporal ordering

Temporal precedence does not automatically establish causality.

```text
Event A occurred before Event B
  ≠
Event A caused Event B
```

Causal semantics remain governed by S101.

## State lifecycle

A State may have a lifecycle represented through transitions.

```text
planned
  ↓
confirmed
  ↓
released
  ↓
executed
  ↓
completed
  ↓
closed
```

The valid state vocabulary is domain-specific.

## State validity

A State should have a temporal validity interval where the distinction matters.

```text
status = in_transit
valid_from = 10:42
valid_to   = 14:17
```

This enables historical reconstruction.

## State snapshot

A State Snapshot represents the state of an Entity or system at a specified reference time.

```text
Inventory Snapshot
  reference_time = 11:00
  quantity = 512
```

A snapshot is not itself necessarily an Event.

## State history

A sequence of state snapshots or transitions can represent the historical evolution of an Entity.

```text
T1: planned
T2: confirmed
T3: released
T4: completed
```

Historical states should remain reconstructable where required.

## Event sourcing is not mandatory

S106 defines event semantics but does not require an event-sourced implementation.

An implementation may store:

```text
current state
state history
events
snapshots
```

according to operational requirements.

## Event and state consistency

Where a State Transition claims to be caused by an Event, the temporal and semantic relationship should be internally consistent.

```text
Event E1: shipment departed
       ↓
State Transition:
ready → in_transit
```

A later correction may supersede the interpretation without rewriting the historical Event unnecessarily.

## Event correction

An Event record may be corrected or reinterpreted while preserving the original information state when auditability matters.

```text
Recorded Event E1
   ↓ correction
Assessment / corrected representation
```

This follows S103/S104 principles.

## Event duplication

Multiple records may refer to the same underlying Event.

```text
ERP record R1
TMS record R2
IoT record R3
      ↓
possible same Event E1
```

This is an Entity/Event Resolution problem and should not be solved by arbitrary deduplication.

## Event identity versus Event record identity

```text
Event
  ≠
Record of Event
```

A single Event can have multiple records, and one record may represent multiple domain events depending on the source semantics.

## Activity

An Activity is a process or action that occurs over an interval and may generate Events and State Transitions.

Examples:

```text
production run
transport
warehouse picking
loading
inspection
```

An Activity may have:

```text
started_at
ended_at
status
participants
outputs
```

## Process versus Event

A Process or Activity may contain multiple Events.

```text
Transport Activity
  ├─ departed
  ├─ checkpoint reached
  ├─ arrived
  └─ delivered
```

Therefore a Process should not be flattened into a single Event when event-level traceability matters.

## Event causation

An Event may have a triggering relationship to a State Transition or Action.

```text
Event
  ↓ triggers
State Transition
```

This is a causal or procedural relationship and must not be confused with mere temporal adjacency.

## Event participation

Events may involve multiple Entities in different roles.

```text
Shipment Departure
  ├─ shipment
  ├─ carrier
  ├─ vehicle
  ├─ origin site
  └─ operator
```

Participation roles should remain explicit rather than encoded only in free text.

## Event location

An Event may occur at or be associated with a Location.

```text
Event E1
  occurred_at_location = Site S1
```

Location identity follows S105.

## Event source

An Event may be reported by one or more Sources.

```text
Event E1
  source = TMS
  corroborated_by = IoT
```

Source provenance follows S104.

## Event epistemic status

The occurrence of an Event may itself be uncertain or inferred.

```text
Observed Event
Inferred Event
Expected Event
Simulated Event
Hypothesized Event
```

The ontology must distinguish a modeled or inferred Event from an actual observed occurrence.

## Forecast events

A Forecast may predict a future Event.

```text
Forecast:
shipment expected to depart at 10:00
```

This is not an actual Departure Event until the event occurs and is appropriately observed or established.

## Scenario events

A Scenario may contain hypothetical Events.

```text
Scenario A
  Event: supplier delay begins at T1
```

Such Events belong to the hypothetical scenario context and must not be inserted into historical reality.

## Counterfactual events

A Counterfactual may represent an Event that did not occur in actual history but is assumed for alternative analysis.

```text
Actual:
no emergency shipment

Counterfactual:
emergency shipment at T1
```

The counterfactual Event must remain epistemically distinct from actual Events.

## Event and Decision loop

Operational SCM often forms a loop:

```text
Event
  ↓
Observation
  ↓
Evaluation
  ↓
Decision
  ↓
Action
  ↓
Outcome
  ↓
Event / Observation
```

S106 provides the temporal backbone for this loop.

## Decision temporal context

A Decision should be evaluated using the information available at Decision Time where historical reconstruction matters.

```text
Events before T1
   ↓ available knowledge
Decision at T1
   ↓
Action at T2
```

Later information should not silently alter the historical decision context.

## State versus KPI

A KPI may summarize one or more States or Events, but is not itself necessarily a State.

```text
Inventory State
   ↓ aggregation
Inventory KPI
```

Derived metric semantics follow S104.

## Temporal granularity

Different SCM concepts require different temporal granularity.

```text
year
month
day
hour
minute
second
continuous interval
```

The ontology should not impose a universal granularity.

## Temporal precision

Precision should not be confused with accuracy.

```text
10:42:31
```

does not prove that the underlying Event time is known to the second.

Temporal uncertainty follows S103.

## Time zone

Time values should retain time-zone or offset semantics where cross-region interpretation matters.

```text
2026-08-14T10:00+09:00
```

A local timestamp without zone context may be ambiguous.

## Calendar semantics

Business calendars, fiscal periods, operating shifts, holidays, and working-time conventions may affect temporal interpretation.

These are contextual semantics and should not be embedded into a generic timestamp primitive.

## Temporal identity interaction

S105 defines identity continuity across time.

S106 defines temporal state and event semantics.

Together:

```text
Entity E1
  ↓
State at T1
  ↓ Event
State at T2
```

An Entity can persist while its State changes.

## Temporal provenance interaction

S104 defines provenance across source and transformation chains.

S106 adds temporal meaning to those chains.

```text
Event occurred_at T1
Observation obtained_at T2
Record processed_at T3
Decision made_at T4
```

This supports complete reconstruction of operational knowledge flow.

## Temporal epistemic interaction

S103 defines epistemic status and time of knowledge.

S106 ensures those assessments can be anchored to time.

```text
At T1:
Forecast F1 existed

At T2:
Actual Event E1 occurred

At T3:
Evaluation compared F1 with E1
```

The forecast should remain a historical forecast rather than becoming an Observation retroactively.

## No universal timestamp

S106 explicitly rejects a universal timestamp semantics such as:

```text
timestamp = "when it happened"
```

without defining what happened and which temporal dimension the timestamp represents.

## No automatic state inference

An Event may suggest a State Transition, but the ontology should not universally infer state changes without domain semantics.

For example:

```text
Shipment departed
  → likely in_transit
```

may be valid in one domain but not another.

The state transition rule should be explicit.

## No retroactive reality mutation

Forecasts, Scenarios, Counterfactuals, and Simulations must not overwrite historical Events or States.

```text
Hypothetical Event
  ≠
Historical Event
```

Likewise, a later Observation may correct knowledge about an earlier Event without changing the fact that the information was unavailable at the earlier Decision Time.

## No mandatory temporal fields on every entity

S106 does not require every Entity to carry:

```text
created_at
updated_at
valid_from
valid_to
occurred_at
```

Temporal properties belong to the semantics of the relevant Event, State, relationship, Observation, or artifact.

## Non-goals

S106 does not define a universal temporal database architecture, event-sourcing implementation, calendar standard, timestamp format, state-machine framework, workflow engine, or causal inference algorithm.
