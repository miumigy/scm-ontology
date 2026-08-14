# S26 — Canonical Demand Concept

## Definition

**Demand** is a requirement for a quantity of an Item over a defined time scope.

## Minimal concept contract

```text
CanonicalDemand
├─ item_id
├─ quantity
├─ unit
├─ period_start
├─ period_end
└─ demand_type
```

Demand is intentionally a semantic requirement, not a forecast algorithm or transaction record.

## Fundamental boundaries

```text
Demand            ≠ Forecast
Demand            ≠ CustomerOrder
Demand            ≠ ActualConsumption
Demand            ≠ Inventory
```

A forecast may be one source or representation used to establish a demand requirement, but forecast semantics are not embedded in the Demand concept.

A customer order may create or contribute to demand, but Order semantics remain separate.

Actual consumption is an observed historical fact and should be represented separately from prospective demand.

## Relationship to Item

```text
Demand
   └─ item_id ──→ Item
```

The time scope is part of Demand semantics. A separate Time entity is not required for the basic concept.

## Planning boundary

S26 deliberately does not define:

- forecasting algorithms
- statistical forecast models
- demand sensing
- aggregation/disaggregation rules
- safety stock
- service-level policy
- allocation logic
- order promising
- consumption recognition rules

Those belong to later planning, policy, or event/observation contracts.

## Why this matters for PSI / S&OP

Demand is one of the principal quantities in a planning graph, but it must remain semantically distinct from inventory and supply. This allows later PSI semantics to represent:

```text
Demand → Supply → Inventory
```

without collapsing fundamentally different facts into a single quantity object.
