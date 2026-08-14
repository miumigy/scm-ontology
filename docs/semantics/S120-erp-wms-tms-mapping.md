# S120 — ERP / WMS / TMS Semantic Mapping

## Purpose

S120 applies the S119 mapping contract to representative enterprise-system patterns without making any vendor schema part of the Core Ontology.

## Mapping principle

```text
ERP / WMS / TMS source semantics
            ↓
      S119 Mapping Contract
            ↓
      Canonical SCM Concept
```

A source object is evidence for a mapping, not a canonical definition.

## Representative patterns

| Source domain | Source example | Canonical target | Notes |
|---|---|---|---|
| ERP | Material master | Material / Item | Identity and descriptive attributes remain distinct |
| ERP | Sales order line | Order / Demand | Requested quantity and commercial identity must not be collapsed |
| ERP | Purchase order line | Order / Supply / Commitment | Direction and commitment semantics depend on context |
| WMS | Stock balance | Inventory | Quantity is contextual to item, location, lot/state and time |
| WMS | Warehouse movement | Flow / Event | Movement event is not itself a persistent inventory state |
| WMS | Pick / pack / ship confirmation | Fulfillment / Execution | Execution status must retain actual event/time semantics |
| TMS | Shipment | Shipment / Flow / Fulfillment | Shipment is an execution object, not a generic Network node |
| TMS | Transport leg | Leg / Route | A leg is part of a route; it is not equivalent to the route itself |
| TMS | Delivery confirmation | Fulfillment / Event | Actual delivery must remain distinct from promised delivery |

## Canonical mapping examples

### ERP Material

```text
ERP Material.material_code
        ↓ identity / normalization
Canonical Material.identifier
```

The ERP code remains a source identifier. S115 Identity Resolution determines whether it resolves to a canonical entity.

### WMS Stock

```text
WMS Stock(item, location, quantity, uom, as_of)
        ↓ unit / reference mapping
Inventory(item, location, quantity, uom, observation_time)
```

A stock balance must not be interpreted as a generic `Item.quantity` attribute. Inventory is contextual state.

### TMS Shipment

```text
TMS Shipment
   ├─ shipment_id → source identifier
   ├─ origin → Location / Node reference
   ├─ destination → Location / Node reference
   ├─ carrier → Actor / Organization reference
   └─ actual delivery → Event / Fulfillment
```

The shipment object may map to execution/flow concepts while preserving its source identity and lifecycle.

## Planned vs actual

A source system may contain both planned and actual timestamps. They must map independently:

```text
planned_departure → planned temporal value
actual_departure  → actual temporal value
promised_delivery → commitment-related temporal value
actual_delivery   → actual event temporal value
```

No mapping rule may collapse these into a single `date` field.

## Source-specific extension

Fields without a canonical semantic equivalent are not forced into Core. They may remain source-specific extensions and retain provenance.

```text
Source Extension
      ↓ optional mapping
Canonical Extension / Contextual Model
```

## Non-goals

S120 does not prescribe SAP, Oracle, Microsoft, Blue Yonder, Manhattan, Kinaxis, or any other vendor schema. It also does not define an enterprise master-data implementation.

## Exit criteria

S120 is complete when representative ERP/WMS/TMS patterns can be mapped using S119 without introducing vendor concepts into Core, while preserving identity, temporal, provenance, and planned/actual semantics.
