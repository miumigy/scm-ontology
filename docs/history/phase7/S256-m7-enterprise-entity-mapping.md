# S256 — M7 Enterprise Entity Mapping Contract

## Purpose

Define the first executable mapping slice from enterprise entity representations to canonical SCM entities without allowing source-system semantics to contaminate the canonical ontology.

## Directional boundary

```text
Enterprise Entity Representation
        ↓
      Adapter
        ↓
 Entity Mapping Decision
        ↓
Canonical Entity Reference
```

The mapping is directional. A canonical entity definition MUST NOT be inferred or expanded from a vendor-specific representation merely because a source field or identifier exists.

## Mapping record

Each entity mapping MUST preserve at least:

- `source_system`
- `source_entity_type`
- `source_entity_id`
- `canonical_entity_type` when mapped
- `canonical_entity_id` when mapped
- `mapping_status`
- `mapping_confidence`
- `provenance`
- `canonical_mutation=false`

## Mapping status

- `mapped`: sufficient evidence supports the selected canonical entity.
- `ambiguous`: multiple canonical interpretations remain plausible; no canonical fact is asserted.
- `unmappable`: the source representation cannot currently be mapped to the existing canonical model.
- `rejected`: the representation is intentionally excluded from canonicalization, for example because it is a vendor-specific classification rather than an SCM entity.

## Cardinality

The adapter MAY represent one-to-one, many-to-one, and one-to-many correspondence between enterprise records and canonical entities. Cardinality describes the mapping relationship; it does not by itself establish a new canonical fact.

## Vendor isolation

Source identifiers such as SAP material numbers, plant codes, vendor codes, WMS warehouse/bin identifiers, or TMS-specific IDs remain enterprise representation and provenance. They MUST NOT become canonical ontology predicates or canonical entity types merely through mapping.

## Semantic gaps

An unmappable or ambiguous entity MUST be classified as a semantic gap before any ontology change is considered. The adapter MUST NOT auto-create ontology concepts to resolve a gap.

## Non-goals

S256 does not define attribute mapping, predicate mapping, vendor connectors, automatic ontology learning, or canonical graph mutation.
