# S23 — Canonical Inventory Concept

## Definition

**Inventory** is a quantity of a defined item held at a defined supply-chain entity.

## Minimal concept contract

```text
CanonicalInventory
├─ item_id
├─ location_id
├─ quantity
└─ unit
```

The concept intentionally represents the existence and quantity of held stock. It does not by itself define inventory policy, replenishment logic, valuation, ownership, availability, or planning status.

## Core/domain alignment

Inventory is a domain concept extending the Core `Entity` primitive. Its measured quantities may be represented through `MetricObservation`, while operational conditions such as available, blocked, reserved, or in-transit require explicit State semantics rather than being implied by the Inventory concept itself.

## Boundaries

Inventory is distinct from:

- **Demand** — a requirement or expected consumption, not held quantity.
- **Order** — a commitment/request, not physical inventory.
- **Shipment** — an occurrence/process representation, not inventory itself.
- **Capacity** — a limit or capability, not held quantity.

## Non-goals

S23 does not define:

- safety stock or reorder points
- valuation/accounting semantics
- ownership or consignment semantics
- available-to-promise semantics
- lot/batch/serial identity
- inventory lifecycle/state vocabulary
- replenishment or optimization algorithms
