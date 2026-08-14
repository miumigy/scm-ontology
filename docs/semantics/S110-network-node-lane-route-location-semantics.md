# S110 — Network, Node, Lane, Route & Location Semantics

S110 defines the semantic structure of the Supply Chain Network and distinguishes Location, Node, Facility, Site, Lane, Route, Path, Network Flow, and Network State.

## Canonical model

```text
Network
 ├─ Location
 │   └─ physical / logical place
 │
 ├─ Node
 │   └─ operational role in the network
 │       └─ Facility / Site / Hub / Port / Customer
 │
 ├─ Lane
 │   └─ permitted or defined connection
 │
 ├─ Route
 │   └─ ordered sequence of movement segments
 │
 └─ Flow
     └─ movement / transformation through the network
```

The central principle is:

```text
Location ≠ Node ≠ Facility ≠ Lane ≠ Route ≠ Flow
```

These concepts may be related, but they represent different semantic dimensions.

## Supply Chain Network

A Supply Chain Network is a structured representation of relevant Nodes, Locations, Lanes, Routes, Resources, Flows, and relationships through which supply-chain operations may occur.

A Network may represent:

```text
physical network
planning network
transport network
production network
information network
```

The Network boundary is contextual.

## Network identity

A Network is an identifiable semantic object that may have:

```text
identity
version
validity
scope
owner / authority
status
```

Network changes should be historically traceable when decisions depend on the network definition.

## Network version

A Network may evolve over time.

```text
Network v1
   ↓
Network v2
```

Historical planning and execution should retain the applicable Network version where material.

## Location

A Location represents a place or spatial reference.

Examples:

```text
address
warehouse coordinates
port
factory site
customer premises
geographic area
GPS position
```

Location answers primarily:

> Where?

It does not by itself answer what operational role exists there.

## Location versus Node

```text
Location
  = place

Node
  = operational role / point in a network
```

A Location may contain multiple Nodes.

Example:

```text
Location: Port Kobe
 ├─ Import Terminal Node
 ├─ Export Terminal Node
 └─ Container Yard Node
```

Conversely, a logical Node may represent an operational aggregation without a unique physical point.

## Geographic Location

A Geographic Location represents a physical position or area in geographic space.

It may include:

```text
latitude
longitude
altitude
address
geofence
administrative area
```

S105 governs identity and resolution of geographic entities.

## Logical Location

A Logical Location represents a non-physical place used for operational semantics.

Examples:

```text
virtual warehouse
planning region
system location
in-transit location
quarantine status location
```

Logical Location must not be silently interpreted as a physical facility.

## Site

A Site is a bounded physical or organizational place at which one or more operational activities, resources, or facilities may exist.

Examples:

```text
manufacturing site
distribution site
customer site
supplier site
```

A Site may contain multiple Facilities or Nodes.

## Facility

A Facility is an operationally identifiable physical structure or establishment capable of hosting Activities, Resources, Inventory, or Flows.

Examples:

```text
factory
warehouse
distribution center
cross-dock
terminal
```

A Facility normally has a Location, but Location itself is not a Facility.

## Node

A Node is an operational point in a Network at which Flow may originate, terminate, transfer, transform, wait, or be controlled.

Examples:

```text
Supplier Node
Factory Node
Warehouse Node
Port Node
Hub Node
Customer Node
```

Node is a network role, not merely a coordinate.

## Node role

A Node may have one or more roles.

```text
production
storage
consolidation
cross-dock
transshipment
customer delivery
supplier origin
```

Roles may change over time.

## Node versus Facility

A Facility is a physical operational entity.

A Node is a network abstraction.

```text
Facility F1
  ↓ represents
Node N1
```

One Facility may support multiple Node roles.

## Node capacity

A Node may expose Capacity for Activities or Flows.

```text
Warehouse Node
  ↓
storage capacity
handling capacity
dock capacity
```

Capacity semantics follow S109.

## Node inventory

A Node may be associated with one or more Stock Points or Inventory positions.

Node and Inventory are not equivalent.

```text
Node
 └─ Stock Point
      └─ Inventory
```

## Node state

A Node may have operational states such as:

```text
open
closed
restricted
congested
maintenance
inactive
```

These states are temporal and contextual.

## Node availability

Node availability determines whether the Node can support a specified Flow or Activity within a context.

Availability may depend on:

```text
calendar
capacity
maintenance
regulation
congestion
security
```

## Lane

A Lane is a defined or permitted connection between Network Nodes for a specified Flow, mode, service, or operational context.

```text
Node A ── Lane L1 ── Node B
```

A Lane may represent a recurring or abstract connection rather than one physical journey.

## Lane versus Route

```text
Lane
  = connection definition

Route
  = ordered movement path composed of one or more connections
```

A Route may traverse multiple Lanes.

## Lane versus Flow

```text
Lane
  = potential / defined connection

Flow
  = actual or planned movement through a connection
```

A Lane can exist without current Flow.

## Lane attributes

A Lane may specify:

```text
origin Node
destination Node
transport mode
carrier eligibility
lead time
transit time
capacity
cost
calendar
service constraints
regulatory constraints
```

These are contextual attributes rather than universal mandatory fields.

## Directed Lane

A Lane may be directional.

```text
A → B
```

The reverse direction:

```text
B → A
```

may have different Capacity, Cost, Lead Time, or Eligibility.

Therefore, undirected physical connectivity must not automatically imply symmetric operational semantics.

## Bidirectional Lane

A Lane may explicitly support both directions.

The two directions may still require separate operational attributes.

## Lane capacity

Lane Capacity represents the usable movement capability of a Lane within a specified time and context.

Examples:

```text
trucks/day
TEU/day
tons/day
ship calls/week
```

Capacity follows S109 and S107 semantics.

## Lane calendar

Lane availability may vary by:

```text
day
season
time window
holiday
curfew
operating hours
```

A Lane is not necessarily continuously available.

## Lane eligibility

A Lane may restrict which:

```text
Products
Modes
Vehicles
Carriers
Orders
Flows
```

can use it.

Eligibility is a Rule/Constraint concept under S107.

## Route

A Route is an ordered sequence of Nodes, Lanes, or movement segments describing a path through a Network.

```text
A → B → C → D
```

Route order is semantically significant.

## Route versus Path

A Path generally represents network connectivity.

A Route may additionally contain operational intent such as:

```text
mode
schedule
stops
carrier
service
constraints
```

The exact distinction may depend on domain usage.

## Route version

Routes may be revised.

```text
Route R1 v1
  ↓
Route R1 v2
```

Historical execution should preserve the Route that was actually selected or executed where relevant.

## Route feasibility

A Route is feasible only under applicable:

```text
Lane availability
Node availability
Capacity
Time windows
Product constraints
Regulatory constraints
Vehicle constraints
```

Feasibility is contextual and may change over time.

## Route selection

Selecting a Route is a Decision under S107.

```text
Candidate Routes
      ↓
Evaluation
      ↓
Decision
      ↓
Selected Route
```

A Route definition itself is not a Decision.

## Planned Route

A Planned Route represents intended routing associated with a Plan or Schedule.

It is not evidence that the Route was actually traveled.

## Actual Route

An Actual Route represents the route actually followed or observed during execution.

```text
Planned Route
      ↓ compare
Actual Route
      ↓
Route Deviation
```

The original Planned Route must remain intact.

## Route deviation

Route Deviation represents a material difference between Planned Route and Actual Route.

Examples:

```text
planned: A → B → C
actual:  A → D → C
```

The deviation may result from an Event, Exception, or Decision.

## Stop

A Stop is an intermediate or terminal operational point within a Route or Flow.

A Stop may involve:

```text
pickup
delivery
loading
unloading
inspection
transshipment
service
```

Stop and Node are not necessarily identical.

## Stop sequence

A Route may specify an ordered Stop sequence.

```text
Stop 1 → Stop 2 → Stop 3
```

Sequence is temporal and operationally significant.

## Leg

A Leg is a movement segment between two relevant points in a Route.

```text
Leg 1: A → B
Leg 2: B → C
```

A Leg may be mapped to a Lane.

## Leg versus Lane

```text
Lane
  = reusable network connection

Leg
  = occurrence / segment within a specific Route or Flow
```

A single Lane may support many Legs over time.

## Transport mode

Transport Mode describes the operational means by which Flow is moved.

Examples:

```text
road
rail
maritime
air
pipeline
inland waterway
multimodal
```

Mode is an attribute of relevant Lane, Route, Leg, or Flow semantics, not a substitute for those objects.

## Multimodal Route

A Route may contain multiple Transport Modes.

```text
Road
 ↓
Maritime
 ↓
Rail
 ↓
Road
```

Mode changes should be represented explicitly at relevant Nodes or transfer points.

## Transshipment Node

A Transshipment Node is a Node at which Flow changes transport service, vehicle, carrier, or mode without necessarily changing its ultimate destination.

## Hub

A Hub is a Node whose operational role includes consolidation, deconsolidation, routing, transfer, or network coordination.

Hub semantics are contextual and do not require a specific physical architecture.

## Port

A Port is a specialized Node or collection of Nodes associated with maritime, air, inland-waterway, or other transport interfaces according to domain context.

A geographic Port Location and an operational Port Node should remain distinguishable.

## Corridor

A Corridor represents a broader network region or sequence of connections through which Flow may commonly travel.

A Corridor may contain multiple Lanes and Routes.

## Network region

A Network Region is a logical or geographic aggregation of Nodes, Locations, Lanes, or Flows.

Examples:

```text
Kansai region
Japan domestic network
Asia-Pacific network
EMEA distribution region
```

Region membership is contextual and may be versioned.

## Network hierarchy

Network abstractions may be nested.

```text
Global Network
 └─ Regional Network
     └─ Country Network
         └─ Site Network
             └─ Node / Lane
```

Hierarchy must not imply physical containment unless explicitly modeled.

## Network topology

Topology describes connectivity and structural relationships among Network elements.

Topology may include:

```text
nodes
lanes
connectivity
directionality
transfer relationships
```

Topology is distinct from operational schedules and current Flow.

## Network state

Network State represents the operational condition of a Network at a reference time.

Examples:

```text
lane closed
port congested
warehouse unavailable
capacity reduced
weather restriction
```

Network State is temporal and contextual.

## Network event

A Network Event represents a material occurrence affecting Network State or operational Flow.

Examples:

```text
port closure
road accident
facility outage
customs hold
capacity reduction
```

Events should remain distinct from persistent Network State.

## Network constraint

Network Constraints limit feasible use of Nodes, Lanes, Routes, or Resources.

Examples:

```text
weight limit
vehicle restriction
operating hours
capacity limit
customs requirement
temperature constraint
```

Constraint semantics follow S107.

## Network policy

Network Policy specifies governed preferences, permissions, prohibitions, or obligations concerning network use.

Examples:

```text
preferred carrier
approved lane
restricted port
mandatory mode
```

Policy and topology must not be conflated.

## Network cost

Network Cost represents a cost associated with using a Node, Lane, Route, Resource, or Flow.

Cost may depend on:

```text
quantity
time
mode
carrier
fuel
congestion
service level
```

Cost is a derived or contextual property, not an inherent universal property of every connection.

## Network lead time

Network Lead Time may be derived from the sequence of relevant activities and movement segments.

```text
Route
 ├─ handling
 ├─ waiting
 ├─ transit
 └─ transfer
```

The underlying temporal events should remain available for auditability.

## Transit time

Transit Time measures elapsed time associated specifically with movement between defined points.

It should not automatically include:

```text
queue time
handling time
customs time
storage time
```

unless explicitly defined.

## Dwell time

Dwell Time measures time that Flow remains at a Node or Location between defined operational events.

Examples:

```text
arrival → departure
receipt → dispatch
```

## Waiting time

Waiting Time represents time during which Flow or Work is waiting for a Resource, Capacity, Event, or decision.

Waiting time is distinct from Transit Time.

## Node-to-node Flow

A Flow may be represented as movement between Nodes.

```text
Node A
  ↓ Flow F1
Node B
```

The Flow may reference the Lane and Route used.

## Flow versus Route

```text
Route
  = intended / selected path

Flow
  = quantity moving through the network
```

A Route can exist without Flow, and multiple Flows can use the same Route.

## Flow versus Lane

```text
Lane
  = network capability / connection

Flow
  = operational movement through it
```

This distinction allows utilization and congestion analysis.

## Flow versus Network State

A Flow is an operational object.

Network State describes conditions affecting that Flow.

```text
Network State:
Lane L1 congested

Flow F1:
1,000 units on L1
```

The two must remain separate.

## Flow path

A Flow Path is the ordered network structure through which a specific Flow travels or is planned to travel.

It may reference:

```text
Nodes
Lanes
Legs
Routes
```

## Planned Flow

A Planned Flow represents intended movement of quantity through the Network.

It belongs to planning semantics from S108 and does not imply actual movement.

## Actual Flow

An Actual Flow represents observed or executed movement.

```text
Planned Flow
    ↓ compare
Actual Flow
```

Differences should be preserved as deviations.

## Network allocation

Network Capacity may be allocated to Flows, Orders, or Plans.

```text
Lane Capacity
   ↓
Flow Allocation
```

Allocation does not necessarily imply actual utilization.

## Network reservation

A Lane, Node, Capacity, or Resource may be reserved for future use.

```text
Node / Lane
  ↓ reservation
Planned Flow
```

Reservation semantics follow S109.

## Network commitment

A Network Commitment may establish an accepted promise concerning:

```text
capacity
route
service
departure
arrival
handling
```

It is distinct from a Route definition.

## Network fulfillment

Fulfillment occurs when relevant Demand, Order, or Commitment requirements are satisfied through network operations.

Network routing is therefore a means of fulfillment, not fulfillment itself.

## Route optimization

Route Optimization is a Decision process that evaluates Candidate Routes against Objectives and Constraints.

```text
Candidate Routes
  ↓
Constraint evaluation
  ↓
Objective evaluation
  ↓
Recommendation
  ↓
Decision
```

S107 governs this semantic boundary.

## Network disruption

A Network Disruption is an Event or State change that materially reduces or changes Network availability or performance.

Examples:

```text
port closure
factory shutdown
lane capacity reduction
transport strike
natural disaster
```

Disruption is not synonymous with delay; the impact must be evaluated contextually.

## Network resilience

Network Resilience is a derived capability or assessment describing the ability of a Network to continue or recover service under disruption.

It is not a primitive physical object.

## Network risk

Network Risk represents assessed uncertainty or exposure concerning future Network performance or availability.

Risk semantics connect to S103 epistemic semantics.

## Network scenario

A Network Scenario represents a hypothetical Network topology or operating condition.

```text
Scenario A
 └─ Lane L1 closed

Scenario B
 └─ Lane L1 open
```

Scenario Networks must not be mistaken for historical actual Networks.

## Counterfactual network

A Counterfactual Network describes how the Network would have operated under an alternative condition.

It is governed by S102 and must remain distinguishable from actual history.

## Network provenance

Network definitions, topology changes, lane restrictions, and route assumptions should be traceable to their source where material.

Examples:

```text
master data
carrier contract
regulation
sensor
traffic provider
planner decision
```

S104 governs provenance and lineage.

## Network temporal validity

Nodes, Lanes, Facilities, Routes, and Policies may have validity intervals.

```text
Lane L1
valid_from = T1
valid_to   = T2
```

A Lane may therefore be valid in one period and unavailable in another.

## Historical network reconstruction

For historical analysis, the applicable Network version and temporal state should be reconstructable.

```text
Order at T1
  ↓
Network v3 at T1
  ↓
Route decision
```

Using today's Network topology to reinterpret historical decisions can produce false conclusions.

## Network identity resolution

Different systems may identify the same physical or logical network object differently.

```text
ERP location code
TMS location code
WMS location code
external port identifier
```

S105 governs identity resolution and equivalence.

## Location hierarchy

Locations may have nested spatial relationships.

```text
Country
 └─ Region
     └─ Site
         └─ Building
             └─ Warehouse
                 └─ Stock Point
```

Hierarchy should not imply that every level is a Node.

## Node aggregation

Multiple operational Nodes may be aggregated into a planning Node.

```text
Warehouse A
Warehouse B
Warehouse C
      ↓ aggregation
Regional DC Node
```

The aggregation rule and scope must be explicit.

## Network abstraction level

A Network may be modeled at different resolutions.

```text
high-level:
Supplier → Factory → Customer

low-level:
Supplier Dock → Carrier → Port → Vessel → Port → DC Dock
```

Both may be valid representations of the same supply chain at different abstraction levels.

## Network flow conservation

Where applicable, Network Flows may require reconciliation across Nodes and Lanes.

```text
inbound
  + production
  - outbound
  - loss
  = inventory change
```

The exact conservation equation depends on process semantics and unit definitions.

## No universal geographic semantics

S110 does not require every Node to have geographic coordinates.

Logical Nodes are valid when physical coordinates are not the intended semantic representation.

## No universal facility-node equivalence

A Facility may expose multiple Nodes, and a Node may represent an abstraction over multiple Facilities.

Therefore:

```text
Facility = Node
```

must not be assumed globally.

## No universal lane-route equivalence

A Lane is a reusable connection definition.

A Route is an ordered path.

Therefore:

```text
Lane = Route
```

must not be assumed.

## No automatic route execution

A Planned or Selected Route does not imply that the route was actually traveled.

Execution semantics follow S108.

## No automatic flow from lane existence

The existence of a Lane does not imply current Flow.

```text
Lane L1 exists
≠
Flow currently using L1
```

## No automatic capacity from topology

Connectivity does not imply unlimited Capacity.

```text
A → B exists
≠
A → B can carry unlimited Flow
```

Capacity and constraints must be modeled separately.

## No automatic availability from location

A physical Location existing does not imply operational availability.

```text
Warehouse exists
≠
Warehouse available for fulfillment now
```

## Closed-loop network operations

S110 connects the network structure to the operational loop:

```text
Network
  ↓
Demand / Order
  ↓
Candidate Routes
  ↓
Constraint / Capacity Evaluation
  ↓
Decision
  ↓
Plan / Schedule
  ↓
Flow / Execution
  ↓
Fulfillment
  ↓
Network Observation
  ↓
Network State Update
  ↓
Replanning
```

Together with S101–S109, this provides a semantic foundation for network-aware SCM planning, optimization, execution, monitoring, and AI decision agents.

## Non-goals

S110 does not define a universal GIS schema, transportation routing algorithm, shortest-path algorithm, network optimization solver, facility-location algorithm, geocoding standard, TMS/WMS schema, or specific network master-data implementation.
