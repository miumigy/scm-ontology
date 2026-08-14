# S109 — Flow, Order, Inventory, Resource & Fulfillment Semantics

S109 defines the core operational semantics connecting Demand, Order, Supply, Flow, Inventory, Capacity, Resource, Allocation, Reservation, Fulfillment, and Service.

## Canonical model

```text
Demand
  ↓
Order
  ↓
Allocation / Commitment
  ↓
Supply / Inventory / Capacity
  ↓
Plan / Schedule
  ↓
Flow / Execution
  ↓
Fulfillment
  ↓
Outcome / Service
```

These concepts represent different aspects of supply-chain reality and must not be collapsed into a single generic `quantity` or `status` model.

## Demand

Demand represents a need, requirement, expectation, or desired quantity of a Product, Service, or Capability during a specified context and time.

Examples:

```text
customer demand
forecast demand
dependent demand
independent demand
safety demand
replacement demand
```

Demand may be observed, forecast, planned, or derived.

## Demand versus Forecast

Forecast is an epistemic prediction about future Demand.

```text
Demand
  = domain need / requirement

Forecast
  = prediction about future demand
```

A Forecast does not become actual Demand merely because it is accurate.

## Demand versus Order

Demand represents a need or requirement.

An Order is a formal request or instruction for a product, service, or fulfillment action.

```text
Demand
  ↓ may generate
Order
```

Demand does not automatically imply an Order.

## Order

An Order is a formal request for fulfillment made by an Actor or system under a defined commercial or operational context.

Examples:

```text
Sales Order
Purchase Order
Transfer Order
Production Order
Transport Order
Work Order
```

Order semantics depend on the domain and must preserve the distinction between requested, promised, planned, and fulfilled quantities.

## Order line

An Order may contain one or more Order Lines representing separately identifiable requested items or services.

```text
Order O1
 ├─ Line L1: Product A, 100
 └─ Line L2: Product B, 50
```

Line-level semantics are important when fulfillment differs by item.

## Requested quantity

Requested Quantity is the quantity specified by an Order or Demand.

```text
requested_quantity = 1,000
```

It is not necessarily the quantity allocated, supplied, shipped, or fulfilled.

## Promised quantity

Promised Quantity is the quantity an Actor has committed to provide under a Commitment or promise.

```text
requested = 1,000
promised  = 800
```

Promised Quantity should remain distinct from Requested Quantity.

## Fulfilled quantity

Fulfilled Quantity is the quantity that has been successfully fulfilled according to the applicable fulfillment semantics.

```text
requested = 1,000
fulfilled = 750
```

Fulfillment may be partial.

## Backorder

A Backorder represents an outstanding portion of an Order or Demand that has not yet been fulfilled and remains intended for future fulfillment.

```text
requested = 1,000
fulfilled = 700
backorder = 300
```

The exact calculation may depend on cancellations, substitutions, and commitments.

## Cancellation

Cancelled Quantity is the portion of requested or committed demand that is no longer expected to be fulfilled because it was explicitly cancelled.

Cancellation should be distinguished from shortage and backorder.

## Supply

Supply represents available, expected, planned, committed, or incoming quantity or capability that can satisfy Demand or Orders.

Examples:

```text
on-hand inventory
purchase order supply
production supply
transfer supply
in-transit supply
scheduled production
```

Supply has temporal and epistemic dimensions.

## Supply versus Inventory

Inventory is a physical or controlled stock position at a Location or other Stock Point.

Supply is broader and may include future or non-stock sources.

```text
Inventory
  ⊂ possible Supply
```

Not all Supply is currently Inventory.

## Supply status

Supply may be:

```text
planned
ordered
committed
in_production
in_transit
available
allocated
consumed
cancelled
```

The vocabulary is domain-specific.

## Flow

A Flow represents movement, transformation, transfer, or propagation of an Entity, Quantity, Material, Product, Information, or other object between states, locations, processes, or actors.

Examples:

```text
material flow
inventory flow
transport flow
production flow
information flow
cash flow
```

Flow semantics must identify what is flowing and through which process or relationship.

## Physical flow

A Physical Flow represents movement or transformation of physical goods or materials.

```text
Supplier
  ↓
Transport
  ↓
Factory
  ↓
Warehouse
  ↓
Customer
```

## Information flow

An Information Flow represents movement or transformation of information, signals, messages, or knowledge.

```text
Sensor
  ↓
TMS
  ↓
Planning System
  ↓
Decision Agent
```

Information Flow is not Physical Flow even when it describes the same physical process.

## Flow versus Activity

An Activity describes work performed over time.

A Flow describes the movement or transformation associated with that work.

```text
Transport Activity
  ↓
Shipment Flow
```

They are related but not equivalent.

## Flow segment

A Flow may be decomposed into segments.

```text
Supplier → Hub
Hub → Warehouse
Warehouse → Store
```

Each segment may have its own:

```text
mode
carrier
location
time
capacity
cost
status
```

## Flow quantity

A Flow Quantity represents the quantity associated with a Flow.

```text
planned flow = 1,000
actual flow = 800
```

Planned and Actual Flow Quantity must remain distinct.

## Flow continuity

Where conservation semantics apply, quantities should remain reconcilable across connected Flow segments.

```text
input
  ↓
transformation / loss / split
  ↓
output
```

Not every Flow is mass-balanced; the governing process semantics determine applicability.

## Split and merge

A Flow may split into multiple downstream Flows or merge from multiple upstream Flows.

```text
          ┌→ F2
F1 ────────┤
          └→ F3
```

```text
F1 ──┐
     ├→ F3
F2 ──┘
```

Allocation and quantity relationships should remain explicit.

## Inventory

Inventory represents a controlled stock position of a Product, Material, Component, Asset, or other stock-managed object at a Stock Point and reference time.

```text
Inventory
  = what is currently held / controlled
```

Inventory is temporally contextual.

## On-hand inventory

On-hand Inventory represents quantity physically or operationally present at a Stock Point according to the relevant inventory definition.

It may require distinctions such as:

```text
available
quality_hold
blocked
damaged
reserved
```

## Available inventory

Available Inventory is the portion of Inventory that is currently eligible for a specified use.

```text
on_hand = 1,000
reserved = 300
blocked = 100
available = 600
```

The exact calculation depends on business rules.

## Reserved inventory

Reserved Inventory represents Inventory protected for a particular Order, Demand, Commitment, or purpose.

Reservation does not imply physical consumption.

## Allocated inventory

Allocated Inventory represents Inventory assigned to satisfy a particular Demand, Order, or Plan.

Allocation may occur before physical picking or shipment.

## Inventory state

Inventory may have multiple dimensions:

```text
quantity
location
ownership
status
condition
lot
serial
availability
reservation
```

A single scalar stock quantity is often insufficient for operational semantics.

## Inventory transaction

An Inventory Transaction records a change to an Inventory position.

Examples:

```text
receipt
issue
transfer
adjustment
consumption
production receipt
return
```

A Transaction is an Event/record concept and must not be confused with the Inventory State itself.

## Inventory snapshot

An Inventory Snapshot represents the inventory state at a reference time.

```text
Stock Point S1
Product P1
reference_time = T1
quantity = 500
```

S106 governs temporal semantics.

## Inventory ownership

Inventory quantity may be associated with an Owner or responsibility context.

```text
company-owned
supplier-owned
customer-owned
consignment
```

Ownership and physical location are distinct.

## Inventory location

Inventory may exist at a Site, Warehouse, Stock Point, Vehicle, Container, or other Location.

S105 governs Location and identity semantics.

## Inventory visibility

Inventory may be:

```text
known
estimated
inferred
unavailable
stale
```

Visibility and epistemic quality follow S103/S104.

## Inventory versus Capacity

Inventory represents stock of an object.

Capacity represents potential ability to perform work, hold quantity, process material, or provide service.

```text
Inventory
  = stock

Capacity
  = ability
```

They should not be represented as the same resource type.

## Capacity

Capacity represents a bounded ability to perform, process, transport, store, or otherwise support an Activity or Flow.

Examples:

```text
factory capacity
warehouse capacity
truck capacity
dock capacity
labor capacity
machine capacity
```

Capacity may be measured in different units.

## Capacity availability

Available Capacity is the portion of capacity that remains usable within a specified time and context.

```text
capacity = 100 hours
allocated = 70 hours
available = 30 hours
```

Availability is contextual.

## Capacity reservation

Capacity may be reserved for a Plan, Order, Commitment, or Activity.

```text
Factory capacity
  ↓ reservation
Production Order
```

Reservation does not imply actual utilization.

## Capacity utilization

Utilization measures actual or planned use relative to available or total capacity.

```text
utilization = used / available
```

The denominator must be explicitly defined.

## Resource

A Resource is an Entity or capability that can be used, consumed, reserved, allocated, or otherwise participate in an Activity or Flow.

Examples:

```text
machine
labor
vehicle
warehouse space
inventory
energy
budget
```

Resource semantics depend on the domain.

## Resource versus Asset

An Asset is an identifiable durable Entity.

A Resource is a role played by an Entity or capability relative to an Activity or Decision.

```text
Truck T1
  = Asset

Truck T1 available transport capacity
  = Resource
```

The same Entity can therefore participate as an Asset and Resource.

## Consumable resource

A Consumable Resource is depleted or transformed through use.

Examples:

```text
raw material
fuel
energy
packaging
```

## Renewable resource

A Renewable Resource can become available again after use or over time.

Examples:

```text
labor hours
machine time
dock capacity
```

The distinction is contextual and temporal.

## Allocation

Allocation assigns a quantity, Resource, Capacity, Inventory, or Supply to satisfy a Demand, Order, Plan, Commitment, or Activity.

```text
Supply S1
  ↓ allocation
Order O1
```

Allocation expresses assignment, not necessarily physical movement.

## Allocation versus Reservation

```text
Reservation
  = protected / held availability

Allocation
  = assigned to a specific purpose
```

An implementation may combine these operationally, but their semantic meanings remain distinct.

## Allocation priority

When Supply or Capacity is scarce, allocation may be governed by:

```text
Policy
Priority
Commitment
Service class
Due date
Optimization Objective
```

S107 governs the decision semantics behind such rules.

## Fulfillment

Fulfillment is the process or result of satisfying an Order, Demand, Commitment, or Service Requirement.

```text
Order
  ↓
Fulfillment
  ↓
fulfilled quantity / service outcome
```

Fulfillment may be partial, complete, substituted, cancelled, or failed.

## Fulfillment versus Shipment

Shipment represents movement of goods.

Fulfillment represents satisfaction of the relevant request or obligation.

A shipment may occur without completing fulfillment, and fulfillment may occur without a conventional shipment.

## Fulfillment line

Fulfillment may be evaluated separately for each Order Line.

```text
Order Line L1
  requested = 100
  fulfilled = 80
```

This supports partial and mixed fulfillment.

## Substitution

Substitution occurs when an alternative Product, Supply source, or service is used to satisfy a Demand or Order according to applicable rules.

```text
requested Product A
       ↓ substitution
fulfilled Product B
```

The substitution relationship should remain explicit.

## Service

Service represents the level or nature of fulfillment experienced by a Demand owner, Customer, or other recipient.

Examples:

```text
on-time delivery
complete delivery
fill rate
availability
response time
```

Service metrics are derived measures and follow S104/S107 semantics.

## Service level

Service Level expresses fulfillment performance relative to a defined Demand, Order, Commitment, or target.

```text
service level = fulfilled / requested
```

The exact numerator and denominator must be defined by context.

## Fill rate

Fill Rate measures the proportion of requested quantity fulfilled according to a specified basis.

```text
requested = 1,000
fulfilled = 900
fill rate = 90%
```

Fill Rate is not universally equivalent to Service Level.

## On-time fulfillment

On-time fulfillment evaluates fulfillment timing against a defined due time or Commitment.

```text
due = T1
fulfilled = T2
```

The tolerance and clock semantics must be explicit.

## Perfect Order

A Perfect Order is a derived performance concept combining multiple fulfillment criteria.

S109 does not mandate a universal formula.

The constituent criteria should be represented separately where analytical transparency matters.

## Demand fulfillment relationship

Demand may be satisfied by one or more Supplies.

```text
Demand D1
  ← fulfillment ←
Supply S1
Supply S2
```

Many-to-many relationships may be required.

## Order fulfillment relationship

An Order may be fulfilled by multiple Fulfillment Events, Shipments, Supplies, or Actions.

```text
Order O1
  ├─ Shipment S1
  ├─ Shipment S2
  └─ Shipment S3
```

One Shipment may also fulfill multiple Orders when business semantics permit.

## Supply allocation relationship

Supply may be allocated across multiple Orders.

```text
Supply = 1,000
  ├─ Order A = 600
  └─ Order B = 400
```

Allocation must remain traceable.

## Inventory and Order relationship

An Order does not necessarily decrement Inventory at creation.

Typical stages may be:

```text
Order
 ↓
Allocation
 ↓
Reservation
 ↓
Picking
 ↓
Issue / Shipment
 ↓
Fulfillment
```

The exact lifecycle is domain-specific.

## Inventory and Flow relationship

Inventory changes may result from Flow Events.

```text
Inbound Flow
  ↓ receipt
Inventory increases
```

```text
Outbound Flow
  ↓ issue
Inventory decreases
```

The relationship should preserve the relevant Event and temporal semantics.

## Capacity and Schedule relationship

A Schedule consumes or reserves Capacity according to the Activity model.

```text
Schedule
  ↓ allocation
Capacity
```

Schedule feasibility should be evaluated against applicable Capacity Constraints from S107.

## Resource contention

Multiple Orders, Plans, or Activities may compete for the same Resource.

```text
Order A ─┐
Order B ─┼→ Resource R1
Order C ─┘
```

Resolution is a Decision problem governed by S107.

## Bottleneck

A Bottleneck is a Resource, Capacity, Flow segment, or process whose effective limitation materially constrains system throughput or service.

Bottleneck status is contextual and may change over time.

## Lead time

Lead Time describes elapsed time between defined temporal events or states.

```text
Order placed
   ↓
Delivery
```

S106 governs the underlying timestamps.

Lead Time should specify which start and end events define it.

## Cycle time

Cycle Time measures elapsed time within a defined process or Activity.

It is not automatically equivalent to Lead Time.

## Queue

A Queue represents Demand, Orders, Work, or Flow units waiting for a Resource, Capacity, or next Process step.

Queue semantics may include:

```text
arrival time
priority
position
waiting time
service start
```

## Queue versus Inventory

A waiting Order or Work item is not automatically Inventory.

Inventory semantics require a stock-managed object or quantity under the applicable domain model.

## Work in Process

Work in Process (WIP) represents material, Product, or work that has entered a production or transformation process but has not reached its completed state.

WIP may be represented as Inventory, Activity state, or both depending on the domain semantics.

## Pipeline supply

Pipeline Supply represents expected future Supply that has not yet become available Inventory.

Examples:

```text
purchase order
scheduled production
in-transit shipment
```

Its epistemic and commitment status must remain explicit.

## Available-to-promise

Available-to-Promise (ATP) represents the quantity that can be promised to Demand under defined Supply, Allocation, Timing, and Policy assumptions.

ATP is a derived decision-support concept, not an independent physical stock type.

## Capable-to-promise

Capable-to-Promise (CTP) incorporates future production or capacity capability into promise evaluation.

CTP therefore depends on Capacity, Schedule, Supply, and Constraint semantics.

## Allocation horizon

Allocation may be constrained by time.

```text
Supply available at T2
Order due at T1
```

A quantity can be physically available in total but unavailable for a particular Order due to temporal constraints.

## Fulfillment horizon

Fulfillment evaluation should consider the relevant due, promise, or service period.

A fulfilled quantity without temporal context is insufficient for on-time service evaluation.

## Reservation expiry

A Reservation may expire or be released according to defined Policy or time semantics.

```text
Reservation
  ↓ expiry
Available Supply
```

The release should be represented as an Event or State Transition where material.

## Inventory reconciliation

Inventory records may differ from physical reality.

```text
System inventory
      ↕
Physical count
```

An Inventory Adjustment may reconcile the representation without implying that the physical quantity changed at the adjustment timestamp.

S103/S104/S106 govern epistemic, provenance, and temporal interpretation.

## Physical versus informational quantity

A quantity in a planning system may represent:

```text
physical quantity
planned quantity
forecast quantity
committed quantity
allocated quantity
promised quantity
reported quantity
```

The quantity meaning must be explicit.

## Unit of measure

Quantities require an applicable Unit of Measure where dimensional interpretation matters.

```text
1,000 kg
500 cases
20 pallets
```

Conversions should preserve source and target units and transformation semantics.

## Quantity uncertainty

Quantities may be estimated, uncertain, or probabilistic.

```text
estimated inventory = 500 ± 20
```

Uncertainty should not be silently represented as exact quantity.

## Flow ownership and custody

Physical possession, legal ownership, and operational responsibility may differ during Flow.

```text
owner
custodian
carrier
operator
```

These roles should remain distinct where material.

## Fulfillment responsibility

The Actor responsible for fulfilling an Order or Commitment may differ from the Actor executing an individual Action.

```text
Supplier
  = fulfillment responsible

Carrier
  = transport executor
```

Responsibility semantics connect to S107 authority and S108 execution.

## Exception fulfillment

Fulfillment may occur through an approved exception, substitution, split delivery, or alternative route.

The exception should remain traceable rather than rewriting the original request.

## Reconciliation chain

A robust SCM model should allow reconciliation across:

```text
Demand
  ↕
Order
  ↕
Allocation
  ↕
Supply
  ↕
Inventory / Capacity
  ↕
Plan / Schedule
  ↕
Flow / Execution
  ↕
Fulfillment
  ↕
Outcome
```

Not every relationship is one-to-one.

## Many-to-many fulfillment

The ontology must permit:

```text
one Demand ← multiple Supply
one Order  ← multiple Shipment
one Supply → multiple Orders
one Shipment → multiple Order Lines
```

This is a fundamental property of real SCM networks.

## No universal quantity conservation

S109 does not assume that every flow conserves quantity exactly.

Transformation, scrap, loss, yield, conversion, packaging, and unit changes may alter quantities.

The applicable process semantics determine conservation rules.

## No automatic inventory decrement

Creating an Order or Allocation does not automatically imply physical Inventory consumption.

Physical inventory changes require the relevant operational Event or transaction semantics.

## No automatic fulfillment from shipment

A Shipment does not automatically mean an Order is fulfilled.

The applicable acceptance, delivery, quantity, quality, and service conditions determine fulfillment.

## No automatic commitment from allocation

Allocation assigns Supply or Capacity but does not necessarily create a Commitment.

Commitment requires the applicable acceptance or obligation semantics from S108.

## No automatic promise from availability

Available Inventory does not automatically imply that a promise has been made to a Customer.

Promise semantics remain governed by Commitment and Decision semantics.

## No automatic capacity feasibility

A Schedule is not feasible merely because nominal Capacity exists.

Timing, Resource contention, setup, sequence, Skills, and other Constraints may matter.

## No automatic service from quantity

Full quantity fulfillment does not automatically imply good Service.

Timing, quality, location, condition, and other requirements may be relevant.

## Closed-loop SCM

S109 completes an important operational loop:

```text
Demand
  ↓
Order
  ↓
Allocation / Commitment
  ↓
Supply / Inventory / Capacity
  ↓
Plan / Schedule
  ↓
Flow / Execution
  ↓
Fulfillment
  ↓
Service / Outcome
  ↓
Observation / Evaluation
  ↓
Decision / Replanning
```

Together with S101–S108, this provides the semantic backbone for a continuously operating SCM Decision and Execution system.

## Non-goals

S109 does not define a universal ERP data model, MRP/DRP algorithm, inventory accounting standard, warehouse-management workflow, transportation-management workflow, APS solver, ATP/CTP algorithm, or fulfillment KPI formula.
