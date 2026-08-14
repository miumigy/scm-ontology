# S29 — Canonical Order Concept

## Definition

**Order** is a commitment or request concerning a quantity of an Item.

## Minimal concept contract

```text
CanonicalOrder
├─ order_id
├─ item_id
├─ quantity
├─ unit
└─ order_type
```

Order represents a transaction/commitment semantic layer. It is deliberately distinct from the planning quantities Demand and Supply.

## Fundamental boundaries

```text
Order             ≠ Demand
Order             ≠ Supply
Order             ≠ Inventory
Order             ≠ Shipment
```

An order may create, confirm, constrain, or contribute to Demand or Supply depending on its type and business context, but those relationships must be explicit.

## Order types

S29 does not canonize CustomerOrder, PurchaseOrder, TransferOrder, ProductionOrder, or other specialized order types as separate concepts.

They may be represented as scoped vocabulary or extensions of Order when additional semantics are required.

## Relationship to Item

```text
Order ──for_item──→ Item
```

Later relationship contracts may connect orders to Demand, Supply, Shipment, Party, Location, or other concepts.

## Non-goals

S29 does not define:

- order lifecycle/state machine
- customer/supplier party semantics
- pricing or commercial terms
- promised dates
- allocation/pegging
- fulfillment
- shipment execution
- demand/supply derivation rules

## Planning and transaction boundary

The intended semantic separation is:

```text
              Order
             /     \
            /       \
       Demand       Supply
          │           │
          └──── Item ─┘
```

The arrows between Order and Demand/Supply are deliberately not implied by S29. They require explicit relationship semantics in a later contract.
