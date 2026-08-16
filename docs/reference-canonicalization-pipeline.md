# Reference Canonicalization Pipeline

This post-M8 slice operationalizes reference canonicalization across multiple source systems.

## Executable adapter

The fixture adapter is available through `scm_ontology.reference_fixture`:

```python
from scm_ontology.reference_fixture import run_fixture

result = run_fixture("examples/reference-canonicalization-pipeline.yaml")
```

The adapter returns immutable source records together with `CanonicalizationResult` values.

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

A shared canonical ID is a canonical **concept** mapping only. It does not prove that source records represent the same enterprise identity, event, fact, or lifecycle object.

## Truth boundary

The adapter performs YAML loading, source-record normalization, explicit mapping construction, registry target validation, and deterministic canonicalization.

It does **not** perform identity resolution, fuzzy matching, semantic inference, fact creation, Canonical Truth mutation, or graph persistence.

Any future write must pass through the governed application transition defined by the M8/S3xx contracts, preserving provenance, scope, temporal semantics, conflicts, and historical state.

## Validation

The fixture in `examples/reference-canonicalization-pipeline.yaml` and regression tests in `tests/test_reference_canonicalization_pipeline.py` plus `tests/test_reference_fixture.py` establish the implementation contract.
