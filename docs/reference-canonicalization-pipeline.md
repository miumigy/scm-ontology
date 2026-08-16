# Reference Canonicalization Pipeline

## Purpose

This slice operationalizes the post-M8 reference canonicalization boundary across multiple source systems.

The pipeline converts **explicit source labels** into canonical concept IDs. It does not perform identity resolution, semantic inference, or Canonical Truth mutation.

## Contract

```text
source record
    |
    v
source label
    |
    | explicit ReferenceMapping
    v
canonical concept ID
    |
    +--> APPLIED
    +--> CONFLICT
    +--> SEMANTIC_GAP
```

### APPLIED

Exactly one canonical target is explicitly declared for the source label.

### CONFLICT

The same source label has multiple explicit canonical targets. The pipeline preserves the conflict rather than choosing one.

### SEMANTIC_GAP

No explicit mapping exists. The pipeline does not infer a target from spelling, similarity, context, or source-system metadata.

## Multi-source boundary

Different source systems may use different labels for the same canonical concept. For example:

- ERP `inventory` → `Inventory`
- WMS `stock` → `Inventory`
- ERP `customer_order` → `Order`

This is reference canonicalization only. A shared canonical ID does **not** imply that the underlying records represent the same enterprise identity, event, fact, or lifecycle object.

## Truth boundary

The result of canonicalization is a derived mapping result. It is not Canonical Truth and must not mutate Canonical Facts automatically.

Any future write must pass through the governed application transition defined by the M8/S3xx contracts, preserving provenance, scope, temporal semantics, conflicts, and historical state.

## Validation

The fixture in `examples/reference-canonicalization-pipeline.yaml` and regression tests in `tests/test_reference_canonicalization_pipeline.py` establish the minimum implementation contract.
