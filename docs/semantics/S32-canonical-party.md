# S32 — Canonical Party Concept

## Definition

**Party** is an organization or actor participating in a supply-chain context.

## Minimal concept contract

```text
CanonicalParty
├─ party_id
├─ name
└─ party_type
```

Party provides the semantic anchor for participants such as suppliers, customers, carriers, manufacturers, and logistics providers without prematurely making each role a separate core concept.

## Fundamental boundaries

```text
Party           ≠ Location
Party           ≠ Order
Party           ≠ Supplier
Party           ≠ Customer
Party           ≠ Carrier
```

Supplier, Customer, Carrier, Manufacturer, LogisticsProvider, and similar terms are roles or scoped vocabulary that may be attached to a Party through later relationship/role contracts.

## Why Party is separate from Location

A Party may operate at multiple Locations, and a Location may host activities for multiple Parties. Therefore party identity must not be encoded as location identity.

## Non-goals

S32 does not define:

- party hierarchy
- legal entity master data
- addresses
- contacts
- commercial agreements
- party roles as a separate lifecycle entity
- ownership or beneficial ownership
- customer/supplier qualification

## Graph impact

S32 establishes the participant layer needed for future transaction and execution semantics:

```text
Party ──role/relationship──→ Order
Party ──role/relationship──→ Location
Party ──role/relationship──→ Shipment
```

The role semantics remain explicit future contracts rather than implicit properties of Party.
