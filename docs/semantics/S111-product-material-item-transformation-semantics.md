# S111 — Product, Material, Item, Specification & Transformation Semantics

S111 defines the semantic distinction between Product, Material, Item, Component, Part, SKU, Specification, Bill of Material, Transformation, Yield, Scrap, Substitute, and Product State.

## Canonical model

```text
Product / Material / Item
        ↓
Specification
        ↓
Composition / BOM
        ↓
Transformation
        ↓
Output Product / Material
        ↓
Product State
```

The central principle is:

```text
Product ≠ SKU ≠ Item ≠ Material ≠ Inventory
Specification ≠ Product
BOM ≠ Inventory
Transformation ≠ Flow
```

These concepts describe different semantic dimensions of what moves, is transformed, specified, stocked, sold, or planned in a supply chain.

## Product

A Product is a class of goods or services that can be offered, produced, procured, transferred, stocked, or fulfilled according to a defined business context. A Product describes what something is intended to be, not a particular physical instance.

## Product identity

A Product should have a stable semantic identity independent of system-specific identifiers where possible. ERP, WMS, TMS, and planning identifiers may be mapped to the canonical Product identity through S105 identity semantics.

## Product instance

A Product Instance represents an identifiable occurrence of a Product, such as a serialized machine, individual vehicle, or specific finished unit. It may have serial, lot, ownership, condition, and location information.

## Item

Item is a contextual term for a discrete object or record representing a Product, Material, Part, or other supply-chain managed entity. Because Item is overloaded across ERP and SCM systems, it should not automatically be treated as a canonical ontology primitive without specifying its intended semantic role.

## Material

Material represents a substance, component, intermediate, or physical input/output used in a production or transformation context. Material may become a Product, remain an intermediate, or be consumed by a process.

## Material versus Product

```text
Material = physical substance / input-output role
Product  = business offering / managed output concept
```

The same physical entity may be both Material and Product in different contexts.

## Component

A Component is an entity used as an input constituent of another Product or Transformation. Component is a relational role, not necessarily a permanent classification.

## SKU

SKU is an operational identification concept representing a stock-managed variant under a particular organization or inventory context.

```text
Product
  ↓ variant / packaging / UoM / market
SKU
```

SKU is contextual and organization-specific; it is not equivalent to canonical Product identity.

## Specification

A Specification defines required or allowed characteristics of a Product, Material, Component, Process Output, or Service. Specification describes requirements; it is not itself the Product.

## Conformance

Conformance indicates whether an observed Product, Material, or Output satisfies a Specification.

```text
Specification → evaluate → Observed State
                         → conformant / nonconformant / unknown
```

## Lot and Serial

A Lot identifies a group or batch of Product or Material. A Serial identifies an individual Product Instance where serialized identity is required. Lot/Serial identity is distinct from Product identity.

## Product state

Product State describes the condition or lifecycle state of a Product or Material at a reference time. Examples: `raw`, `in_process`, `finished`, `released`, `reserved`, `shipped`, `returned`, `scrapped`.

State must not be confused with Product identity.

## Transformation

A Transformation is an Activity or process that changes one or more input entities into one or more output entities, states, or quantities.

```text
Input Material → Transformation → Output Product
```

Transformation semantics connect S111 to S109 Flow and S108 Execution.

## Transformation versus Flow

```text
Transformation = change / process
Flow           = movement / propagation
```

A Transformation may occur without spatial movement. A Flow may occur without transforming the Product.

## Bill of Material

A Bill of Material (BOM) defines a Product structure by specifying required Components and quantities for a particular Product, context, and version.

```text
Finished Product
 ├─ Component A × 2
 ├─ Component B × 1
 └─ Component C × 4
```

A BOM is a definition, not the physical inventory consumed by production.

## BOM version and effectivity

BOMs are versioned structures and may be effective by date, lot, serial, site, market, or other context. S106 governs temporal semantics and S107 governs applicability rules.

## Actual consumption

Actual Consumption records the quantity of Material or Component actually consumed by an Execution or Transformation.

```text
BOM requirement = 10 kg
Actual consumption = 11.2 kg
```

The variance remains observable.

## Yield and Scrap

Yield represents the relationship between useful Output and relevant Input for a defined Transformation. Scrap represents input or intermediate material rendered unavailable for the intended useful output.

Scrap should be distinguished from normal yield loss, rework, return, by-product, and co-product.

## By-product and Co-product

A By-product is an output that is not the primary intended Product but has recognized operational or economic significance. A Co-product is one of multiple intentionally valuable outputs produced by a Transformation.

## Rework

Rework is an Activity or Transformation intended to correct, modify, or bring an existing Output toward the required Specification.

## Substitute component

A Substitute Component is an alternative Component permitted to satisfy a BOM or production requirement under specified Rules or Constraints. Substitution must preserve the original requirement and applicable rule.

## Alternate BOM

An Alternate BOM is an alternative Product structure that may be selected under defined conditions. The selection is a Decision governed by S107.

## Recipe and Routing

A Recipe is a process-oriented structure specifying inputs, transformations, conditions, and outputs, often used for process manufacturing. Routing defines an ordered or constrained sequence of Operations used to produce or transform a Product. Neither is an executed Schedule.

## Work center

A Work Center is an operational capability or Resource context through which an Operation can be executed. Work Center semantics connect to S109 Resource and Capacity.

## Product-process and product-flow compatibility

A Product may only be transformed through compatible Processes, Operations, Resources, and Specifications. It may also have Flow constraints such as temperature, hazardous classification, shelf life, packaging, mode restrictions, or handling requirements.

These are Constraint/Rule semantics under S107 and interact with S110 Network semantics.

## Packaging and Unit of Measure

Packaging represents a physical or logical containment/presentation structure associated with a Product or Material. Unit of Measure defines the dimensional basis for quantity representation. Conversions specify correspondence between units under a defined context.

Packaging and UoM may change an operational SKU without changing the underlying Product identity.

## Product hierarchy

```text
Product Family
 └─ Product
     └─ Variant
         └─ SKU
```

Each relationship must preserve its semantic reason.

## Product equivalence versus substitution

```text
Equivalent Product = semantically interchangeable under defined context
Substitute Product = alternative permitted for a specific requirement
```

Substitution does not imply global equivalence.

## Product transformation graph

Product structures and transformations may form a directed graph.

```text
Raw A ─┐
Raw B ─┼→ Intermediate C ─→ Finished D
Raw E ─┘
```

This graph supports traceability, planning, costing, and impact analysis.

## Genealogy

Genealogy represents traceable relationships between actual input Lots/Serials and output Lots/Serials across Transformations.

```text
Input Lot L1
Input Lot L2
      ↓
Transformation T1
      ↓
Output Lot L3
```

Genealogy is distinct from BOM definition.

## BOM versus Genealogy

```text
BOM       = what should be used
Genealogy = what was actually used / produced
```

## Planned versus actual composition

A Plan may specify intended composition. Execution may produce actual composition that differs because of substitution, yield, scrap, or deviation. Both must remain traceable.

## Engineering change

An Engineering Change is a Decision/Event that modifies Product Specifications, BOMs, Routings, or related definitions. Historical execution should preserve the definitions applicable at execution time.

## Change effectivity

A change may apply based on date, lot, serial, order, site, market, or revision. Effectivity is a Rule over Product definitions and execution context.

## Product master versus canonical Product

A Product Master in an enterprise system is an implementation representation. The canonical Product concept is the semantic entity independent of a particular ERP or WMS representation.

## No universal Item semantics

Because `Item` is overloaded across SCM systems, implementations must define whether it means Product, SKU, Material, Product Instance, Inventory identity, or Order line item.

## No automatic BOM consumption

A BOM requirement does not imply that the listed quantity was actually consumed. Actual Consumption belongs to Execution/Genealogy semantics.

## No automatic transformation from movement

Movement of a Product does not imply that the Product was transformed. A Transport Flow may preserve Product identity.

## No automatic product equivalence from matching description

Two items with similar names are not automatically equivalent Products. Identity resolution must use defined semantic criteria.

## No automatic quality from product identity

Product identity does not guarantee a particular Quality State. Quality is contextual and temporal.

## No automatic inventory from product existence

The existence of a Product does not imply that Inventory exists.

## No automatic supply from BOM

A BOM defines requirements; it does not prove Supply availability.

## No automatic feasibility from product structure

A valid BOM does not imply that production is feasible. Capacity, Resource, Material availability, Network, Policy, and other Constraints must be evaluated.

## Closed-loop product semantics

```text
Demand
  ↓
Product / Specification
  ↓
BOM / Routing / Constraints
  ↓
Supply / Inventory / Capacity
  ↓
Plan / Schedule
  ↓
Transformation / Flow / Execution
  ↓
Actual Product State / Genealogy
  ↓
Fulfillment / Outcome
  ↓
Observation / Evaluation
  ↓
Change / Replanning
```

Together with S101–S110, this establishes the semantic foundation for product-aware SCM planning, execution, traceability, quality, substitution, and AI reasoning.

## Non-goals

S111 does not define a universal ERP material master, PLM schema, BOM implementation, MES schema, MRP algorithm, costing method, quality-management standard, or product lifecycle-management workflow.
