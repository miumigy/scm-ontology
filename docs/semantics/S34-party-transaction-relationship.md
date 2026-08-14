# S34 — Party ↔ Transaction Relationship Contract

## Purpose

S34 connects the contextual Party Role layer to transaction and physical-flow concepts without making roles intrinsic properties of Party.

## Canonical relationship contract

```text
PartyTransactionRelationship
├─ party_role
├─ predicate
└─ transaction_type
```

Initial canonical relationships:

```text
customer     ──places───→ CustomerOrder
supplier     ──receives─→ PurchaseOrder
manufacturer ──creates───→ ProductionOrder
carrier      ──executes─→ Shipment
```

## Semantic boundaries

These relationships express contextual business roles. They do not assert that every party with a role participates in every transaction of that type.

They also do not define:

- order lifecycle
- shipment status
- legal responsibility
- ownership
- contractual terms
- fulfillment completion
- inventory posting

Those semantics require separate contracts.

## Why direction matters

`customer places CustomerOrder` is directional and expresses an initiating role.

`supplier receives PurchaseOrder` expresses a receiving role rather than ownership of the order.

`manufacturer creates ProductionOrder` identifies the party role responsible for creating the production transaction.

`carrier executes Shipment` identifies the operational execution role and does not imply that the carrier owns the goods.

## Graph impact

```text
Party
  │
  └─ PartyRole
       │
       ├─ customer ──────places─────→ CustomerOrder
       ├─ supplier ─────receives────→ PurchaseOrder
       ├─ manufacturer ─creates─────→ ProductionOrder
       └─ carrier ──────executes────→ Shipment

CustomerOrder ──contributes_to──→ Demand
PurchaseOrder ──creates─────────→ Supply
ProductionOrder ──creates───────→ Supply
```

This establishes an explicit participant-to-transaction layer while preserving the separation between identity, role, transaction, planning quantity, and physical flow.
