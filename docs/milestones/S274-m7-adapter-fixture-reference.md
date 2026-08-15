# S274 — M7 Adapter Fixture / Reference Implementation

## Purpose

Provide a vendor-neutral Enterprise Adapter Fixture that exercises the M7 Canonicalization boundary end to end without importing vendor semantics into the Canonical Ontology.

## Fixture scope

The fixture represents a minimal enterprise dataset with:

- material master representation;
- supplier master representation;
- site / plant representation;
- enterprise identifiers;
- an enterprise material classification;
- supplier-to-material supply representation;
- material-to-site stocking representation.

All source fields are explicitly enterprise representations. Their names, codes, and classifications MUST NOT be treated as Canonical Semantics by themselves.

## Reference mapping

```text
Enterprise Material   → Canonical Material
Enterprise Supplier   → Canonical Supplier
Enterprise Site       → Canonical Site

Enterprise supply relation
        → approved Canonical supply predicate

Enterprise stocking relation
        → approved Canonical stocking predicate
```

The fixture MUST use only mappings that already exist in the Canonical Ontology and approved mapping configuration. It MUST NOT require a new canonical concept.

## Provenance

Every mapped output MUST retain enough provenance to identify:

- fixture/source record;
- source field or relation;
- adapter version;
- mapping configuration version;
- mapping decision reference.

## Expected behavior

A conformant reference implementation MUST:

1. produce deterministic mapping results for the fixed fixture;
2. preserve Enterprise-to-Canonical directionality;
3. preserve provenance;
4. preserve mapping confidence;
5. represent unsupported or ambiguous input explicitly;
6. leave Canonical Facts unchanged as an implicit side effect.

## Negative fixture cases

The fixture SHOULD include cases for:

- vendor-style classification with no approved Canonical mapping;
- ambiguous enterprise label;
- missing provenance;
- unmappable enterprise field.

These cases MUST result in explicit mapping outcomes or Semantic Gap classifications rather than automatic Canonical expansion.

## Canonical contamination boundary

The reference implementation:

- MUST NOT create a new canonical entity, attribute, or predicate automatically;
- MUST NOT mutate canonical facts;
- MUST NOT infer Canonical Truth from source labels or vendor-style codes alone;
- MUST NOT promote an enterprise classification into Canonical Semantics without an approved mapping;
- MUST NOT silently discard unmappable or ambiguous input.

## Testability

The fixture MUST be stable and versioned so that S273 conformance checks and later end-to-end tests can replay the same input and compare results without relying on live enterprise systems.

## Non-goals

S274 does not define SAP, ERP, WMS, TMS, APS, or other vendor connectors. It does not define production ingestion, automatic mapping discovery, ontology learning, Canonical Fact ingestion, or graph mutation.
