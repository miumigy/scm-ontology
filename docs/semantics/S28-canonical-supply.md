# S28 — Canonical Supply Concept

## Definition

**Supply** is a quantity of an Item that is planned or expected to become supply within a defined time scope.

## Minimal concept contract

```text
CanonicalSupply
├─ item_id
├─ quantity
├─ unit
├─ period_start
├─ period_end
└─ supply_type
```

Supply is deliberately a semantic quantity over time. It does not prescribe how the supply is created.

## Fundamental boundaries

```text
Supply            ≠ Production
Supply            ≠ PurchaseOrder
Supply            ≠ Shipment
Supply            ≠ Inventory
Supply            ≠ Capacity
```

Production, procurement, transfer, and other mechanisms may create or contribute to supply, but their lifecycle and transaction semantics remain separate.

## Relationship to Item

```text
Supply
  └─ item_id ──→ Item
```

This establishes the planning-side counterpart to Demand:

```text
Demand ──for_item──→ Item ←──for_item── Supply
```

## Planning boundary

S28 does not define:

- production orders
- purchase orders
- transfer orders
- shipment execution
- capacity consumption
- lead-time calculation
- sourcing rules
- allocation or pegging
- finite-capacity planning

These belong to later transaction, process, relationship, or planning contracts.

## PSI implication

Supply and Demand are intentionally symmetrical quantity concepts while remaining semantically distinct. This allows later PSI semantics to introduce inventory as a stock state/observation rather than collapsing demand, supply, and inventory into one quantity model.
