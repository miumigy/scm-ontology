# S31 — Canonical Shipment Concept

## Definition

**Shipment** is a physical movement or handoff of an Item between two distinct Locations.

## Minimal concept contract

```text
CanonicalShipment
├─ shipment_id
├─ item_id
├─ quantity
├─ unit
├─ origin_location_id
└─ destination_location_id
```

Shipment is an execution/flow concept. It describes the movement or handoff itself, not the inventory resulting from the movement.

## Fundamental boundaries

```text
Shipment          ≠ Inventory
Shipment          ≠ Supply
Shipment          ≠ Order
Shipment          ≠ Route
Shipment          ≠ TransportMode
```

A shipment may fulfill an Order or execute part of a Supply plan, but those relationships are explicit and are not implied by S31.

## Relationship to Item and Location

```text
Shipment ──for_item──→ Item
Shipment ──from───────→ Location
Shipment ──to─────────→ Location
```

Origin and destination are deliberately represented as references to the canonical Location concept rather than embedding address or geographic semantics.

## Physical-flow boundary

S31 does not define:

- carrier
- vehicle
- transport mode
- route/lane
- shipment status lifecycle
- departure/arrival events
- freight cost
- emissions
- customs
- proof of delivery
- inventory posting

Those are later concepts, states, events, or relationship contracts.

## SCM Graph impact

S31 introduces the first explicit physical-flow edge between canonical Locations:

```text
Location A
    │
    │ from
    ▼
 Shipment
    │
    │ to
    ▼
Location B
```

The Shipment remains attached to an Item, creating the basis for a later SCM network graph without prematurely defining route optimization or transportation execution details.
