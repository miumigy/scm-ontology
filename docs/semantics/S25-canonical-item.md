# S25 — Canonical Item Concept

## Definition

**Item** is a definable thing that can be identified, planned, moved, transformed, or held within the supply chain.

## Minimal concept contract

```text
CanonicalItem
├─ item_id
├─ item_type
└─ name
```

Item is deliberately broader than Product or Material. Those terms can be represented as domain vocabulary or scoped extensions of Item when their semantics require additional constraints.

## Relationship to Inventory

Inventory represents a quantity of an Item held at a Location.

```text
Inventory
├─ item_id     ──→ Item
└─ location_id ──→ Location
```

This establishes the first reusable SCM semantic triangle:

```text
          Item
         /    \
        /      \
   Inventory ── Location
```

## Boundaries

Item is distinct from:

- **Inventory** — a held quantity of an item at a location.
- **Demand** — a requirement or expected consumption involving an item.
- **Order** — a commitment or request involving an item.
- **Shipment** — movement/fulfillment semantics involving an item.

## Product / Material / SKU

S25 does not make Product, Material, SKU, Part, Component, or Finished Good separate Core concepts.

They may become scoped vocabulary terms or extensions of Item when their distinctions are semantically material.

## Non-goals

S25 does not define:

- bill of materials
- item hierarchy
- product lifecycle
- SKU coding rules
- material classification
- product master governance
- demand or supply planning logic
- substitution semantics
