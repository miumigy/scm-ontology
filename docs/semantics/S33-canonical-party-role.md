# S33 — Canonical Party Role Contract

## Definition

A **Party Role** describes the role played by a canonical Party within an explicit supply-chain context.

## Minimal contract

```text
CanonicalPartyRole
├─ party_id
├─ role
└─ context
```

## Initial scoped vocabulary

```text
supplier
customer
manufacturer
carrier
logistics_provider
```

These are role values, not separate core entities.

## Semantic boundary

The same Party may play multiple roles:

```text
Party-001 ──supplier──→ Context-A
Party-001 ──customer──→ Context-B
Party-001 ──carrier───→ Context-C
```

Role is therefore contextual rather than an intrinsic replacement for Party identity.

## Relationship direction

S33 establishes the semantic meaning of `Party plays_role Role`, but does not yet define concrete relationship contracts to Order, Location, Shipment, or other concepts.

Those links remain explicit future contracts.

## Non-goals

S33 does not define:

- legal entity hierarchy
- ownership
- organizational structure
- master-data governance
- contracts or commercial agreements
- role lifecycle
- party qualification
- role exclusivity

## Graph impact

The participant layer becomes:

```text
Party
  │
  └──plays_role──→ PartyRole
                       │
                       └── role = supplier/customer/carrier/...
```

This keeps Party identity stable while allowing SCM context to determine how the Party participates.
