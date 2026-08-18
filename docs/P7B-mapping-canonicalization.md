# P7-B — Mapping / Canonicalization Runtime

## Purpose

P7-B is the second **Phase 7 (SCM OS Real Data Plane)** slice. It turns the
`SourceEvidence` produced by the P7-A Reference Data Adapter
(`src/scm_ontology/reference_data_adapter.py`) into explicit, deterministic
**source-to-canonical mapping decisions** without embedding source-system
semantics in the Canonical Ontology.

```text
SourceEvidence (P7-A)
        ↓
 MappingRule (explicit, versioned)
        ↓
 MappingCanonicalizer
        ↓
 CanonicalizationResult  (mapped / ambiguous / unmappable / rejected / ...)
        │
        └─ canonical_mutation = false  (a result, never a Canonical Fact)
```

P7-B consumes the P7-A evidence directly (reuse before adding contracts) and
emits S262-compatible `CanonicalizationResult` records. It maps entity, attribute,
and predicate representations per the M8 contracts **S256 / S257 / S258**, and
classifies gaps per the S255 semantic-gap contract.

## Contract

`src/scm_ontology/mapping_canonicalization_runtime.py` defines:

- **`MappingRule`** — a versioned, explicit rule per source system with an
  `EntityMapping`, `AttributeMapping`s, `PredicateMapping`s, and
  `rejected_fields`.
- **`Transform`** — explicit code/unit representation normalization. It never
  invents business meaning; an unknown source code is a gap, not a promotion.
- **`MappingCanonicalizer`** — deterministically governs every `SourceEvidence`
  record against its source system's rule; a record with no rule fails closed as
  `unmappable`.
- **`CanonicalizationResult`** — the S262 mapping decision with
  `result_id`, `decision_state`, `mapping_confidence`, `provenance`, `reason`,
  `mapping_rule_id`, `semantic_gap`, `transformation_metadata`, and
  `canonical_mutation = False`.
- **`MappingRun`** — a deterministic aggregate (`mapped_count`, `gap_count`,
  content-sorted JSON).

### Decision states (S261/S262 vocabulary)

`mapped`, `ambiguous`, `unmappable`, `rejected`, `unsupported`,
`insufficient_evidence`, `conflicting_semantics`. A `mapped` result MUST carry a
`canonical_type` and `canonical_target` — a canonical *reference*, never a fact.

### Semantic gap classification (S255)

`no_canonical_target`, `ambiguous_mapping`, `vendor_specific_semantics`,
`granularity_mismatch`, `temporal_mismatch`, `authority_insufficient`.

## Mapping boundaries

- **Entity (S256)**: a source entity type maps to an existing canonical entity
  type; the source identifier remains provenance, never a canonical predicate or
  entity type by itself.
- **Attribute (S257)**: a source field maps to an existing canonical attribute;
  field names are not semantics. Value `Transform`s normalize representation
  only (unit/code) and never add derived business meaning.
- **Predicate (S258)**: a source relation maps to an existing canonical predicate
  with explicit subject/target endpoint fields; a missing endpoint is a `rejected`
  gap, never an inferred relation.
- **Rejected**: a configured vendor-only / control field present in the source
  payload blocks the record instead of being silently promoted.

## Fail-closed behavior

The runtime MUST reject:

- a `MappingRule` with blank fields, duplicate attribute source fields, a field
  both mapped and rejected, or an entity id field marked rejected;
- a duplicate rule for the same source system;
- a `Mapped` result without `canonical_type` / `canonical_target`;
- any result with `canonical_mutation = True` (P7-B never mutates truth);
- a record with no rule (→ `unmappable`), a missing required source field
  (→ `unmappable`), a missing entity-id (→ `authority_insufficient`), or an
  unknown transform code (→ `vendor_specific_semantics`).

## Deterministic reference path

`run_reference_mapping_path()` consumes `run_reference_data_adapter_path()`
(ERP `@csv` → Material, WMS `@json` → InventoryPosition, TMS `@sql` → Shipment
with a `carriedBy` predicate edge) and maps all 6 evidence records
deterministically, with identical JSON across runs.

## Non-goals

P7-B does not:

- resolve identity across source systems (P7-C);
- run data-quality / freshness gates (P7-D);
- mutate Canonical Truth, the Canonical Graph, or the Canonical Ontology;
- infer a mapping from field names, spelling, similarity, or adapter success;
- promote a vendor classification or control field to canonical semantics;
- add vendor connectors, database drivers, or web dependencies (stdlib only).
