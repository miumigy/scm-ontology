# S119 — Enterprise Semantic Mapping Contract

## Purpose

S119 defines the boundary between source-system semantics and the SCM Ontology Canonical Model.

The contract allows SAP, ERP, WMS, TMS, MES, APS, S&OP, PSI, BI, IoT, and transportation data to map into canonical concepts without importing source-specific vocabulary into the Core Ontology.

## Canonical pipeline

```text
Enterprise Source
      ↓
Source Dataset / Field
      ↓
Source Concept
      ↓
Mapping Specification
      ↓
Transformation
      ↓
Canonical Concept / Attribute / Value
      ↓
Canonical Instance
      ↓
Provenance + Identity Resolution
```

## Mapping is not identity

A source field name is not evidence that the source concept and canonical concept are identical.

```text
SAP Material
WMS Item
ERP Product
      ↓ semantic mapping
Canonical Material / Product / Item
```

The mapping must record its source, rule, confidence/status, and effective validity where applicable.

## Minimum mapping semantics

A mapping specification should be able to express:

- source system / namespace
- source concept
- source field or attribute
- canonical concept
- canonical attribute
- transformation expression or operation
- mapping status
- confidence when the mapping is inferential
- effective validity interval
- provenance reference
- identity-resolution reference where the mapping resolves an entity

## Mapping statuses

```text
proposed
reviewed
approved
deprecated
rejected
```

A proposed mapping must not silently become an approved canonical assertion.

## Transformation semantics

A transformation may include:

- rename
- type conversion
- unit conversion
- code translation
- normalization
- composition
- decomposition
- aggregation
- derivation
- identity resolution

A transformation changes representation or derives meaning; it does not erase source provenance.

## Source vs canonical truth

The mapping layer must preserve the source value and its provenance whenever practical.

```text
Source Value
    ↓
Transformation
    ↓
Canonical Value
```

The canonical value is not evidence that the source value was wrong. Both may be needed for lineage, reconciliation, and audit.

## Identity integration

S115 remains authoritative for identity semantics.

```text
Source Identifier
      ↓
Identity Resolution
      ↓
Canonical Reference
```

A mapping must not create canonical identity merely because two source codes have the same lexical value.

## Epistemic integration

S103 remains authoritative for epistemic status.

A mapping can carry or transform values, but must not silently upgrade:

```text
estimate → fact
inference → observation
prediction → actual
hypothesis → confirmed fact
```

## Temporal integration

S106 remains authoritative for time semantics. Mapping specifications may themselves have validity/effective periods, but must not collapse source effective time, transaction time, observation time, planned time, or actual time.

## Provenance integration

S104 remains authoritative for lineage.

At minimum, a canonical mapped value should be traceable to:

```text
source
→ mapping
→ transformation
→ canonical value
```

## Vendor neutrality

Examples such as SAP Material or WMS Item are mapping-source examples only. They are not Core Ontology concepts.

Vendor-specific extensions belong outside the Core namespace.

## Non-goals

S119 does not define:

- SAP-specific mappings
- WMS/TMS vendor schemas
- universal ETL syntax
- business-specific reconciliation policies
- graph storage syntax
- automated semantic matching algorithms

Those are implementation layers above this contract.

## Exit criteria

S119 is complete when an implementation can describe a source-to-canonical mapping without changing the Core Ontology, while preserving transformation, identity, temporal, epistemic, and provenance semantics.
