# S30 — Order ↔ Demand / Supply Relationship Contract

## Purpose

S30 makes the previously deferred bridge between transactional Order concepts and planning quantities explicit.

## Canonical bridge contract

```text
OrderPlanningBridge
├─ order_type
├─ predicate
└─ planning_type
```

Initial canonical bridges:

```text
CustomerOrder  ──contributes_to──→ Demand
PurchaseOrder  ──creates─────────→ Supply
ProductionOrder ──creates────────→ Supply
```

## Why the bridge is explicit

An Order is not automatically Demand or Supply. The bridge expresses a scoped business meaning that connects a transaction/commitment to a planning quantity.

This prevents the common semantic collapse:

```text
Order == Demand == Supply
```

which would make later planning, execution, and reconciliation semantics ambiguous.

## Direction and semantics

The predicate direction matters.

`CustomerOrder contributes_to Demand` means the order is a source/contributor to a demand requirement. It does not mean every Demand must originate from an order.

`PurchaseOrder creates Supply` and `ProductionOrder creates Supply` identify mechanisms by which planned/expected supply can be established. They do not define execution completion or physical inventory creation.

## Boundary conditions

S30 does not define:

- one-to-one or one-to-many cardinality
- pegging/allocation
- order lifecycle
- confirmation semantics
- cancellation effects
- forecast-to-demand derivation
- shipment fulfillment
- inventory posting
- production execution

These require separate semantic contracts.

## Graph impact

The planning/transaction bridge now has an explicit shape:

```text
CustomerOrder ──contributes_to──→ Demand ──for_item──→ Item

PurchaseOrder ──creates─────────→ Supply ──for_item──→ Item
ProductionOrder ──creates────────→ Supply

Inventory ──for_item────────────→ Item
Inventory ──held_at─────────────→ Location
```

This is the first explicit bridge between transaction semantics and PSI planning semantics.
