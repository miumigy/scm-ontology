# S35 — Canonical Event Concept

## Definition

**Event** is a fact that an event of a given type occurred for a subject at a defined time.

## Minimal concept contract

```text
CanonicalEvent
├─ event_id
├─ event_type
├─ occurred_at
└─ subject_id
```

Event represents an occurrence, not a current state. The subject may be a Shipment, Order, Inventory, ProductionOrder, or another canonical concept.

## Fundamental boundaries

```text
Event  ≠ Entity
Event  ≠ Relationship
Event  ≠ State
```

An Event records that something happened. It does not by itself define the current state resulting from that occurrence.

## Example vocabulary

```text
ShipmentDeparted
ShipmentArrived
OrderCreated
OrderConfirmed
ProductionStarted
ProductionCompleted
InventoryReceived
InventoryIssued
```

These are event types/vocabulary examples, not separate canonical entities in S35.

## Event versus State

```text
Shipment
   │
   ├─ event: departed @ 09:30
   ├─ event: arrived  @ 14:10
   │
   └─ current state: arrived
```

The event history and current state remain separate semantic layers.

## Non-goals

S35 does not define:

- event ordering or causality
- event sourcing implementation
- state machines
- event schema per business process
- actor attribution
- location attribution
- event payloads
- timestamps beyond the canonical occurrence time
- derived state rules

Those require later contracts.

## Graph impact

S35 introduces a temporal fact layer:

```text
Event
  │
  └─ subject_id ──→ Shipment / Order / Inventory / ...
```

This allows SCM Graph to represent not only what exists and how things relate, but also **what happened and when**.
