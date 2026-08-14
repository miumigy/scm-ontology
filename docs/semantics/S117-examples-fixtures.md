# S117 — Examples / Fixtures

S117 provides representative fixtures that exercise the S113-S116 canonical model without introducing vendor-specific ontology concepts.

## Fixture goals

The examples demonstrate:

- Physical / Information / Decision / Semantic dimensions
- Primitive/Core/Derived layering
- Typed attributes and cardinality
- Canonical relationship signatures
- Identifier and canonical reference separation
- Provenance and epistemic status
- Planned / Actual / Observed / Predicted / Inferred distinctions

## Important boundary

Fixtures are examples of valid intended usage. They are not a second ontology and are not exhaustive.

A fixture may mention a source such as WMS or ERP to demonstrate provenance or source identity. That does **not** promote the source-system vocabulary into the Core Ontology.

## Primitive vs derived example

`Inventory` is modeled as a Core concept. `ServiceLevel` is modeled as Derived and is represented through a measurement-derived value rather than as a physical object.

This preserves the rule:

```text
Inventory
   ↓ measurement
Measurement
   ↓ derivation
ServiceLevel
```

## Epistemic example

The second fixture deliberately keeps prediction, observation, plan, actual, and hypothesis separate. Identical subjects do not imply identical semantic status.

```text
Prediction  ≠ Observation
Plan        ≠ Actual
Observation ≠ Inference
Inference   ≠ Fact
```

## Provenance example

The fixture records source-system identity as provenance rather than changing the canonical meaning of the entity.

```text
WMS identifier
      ↓
Source Identity
      ↓
Canonical Reference
      ↓
Inventory
```

## Exit criteria

S117 is complete when representative fixtures cover the core dimensions and semantic boundaries needed for S118 validation, while remaining independent of any particular enterprise schema or vendor implementation.
