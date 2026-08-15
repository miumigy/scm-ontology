# S258 — M7 Enterprise Predicate / Relation Mapping Contract

## Purpose

Define a safe mapping boundary from an enterprise relationship representation to an existing canonical predicate without importing vendor-specific relationship semantics into the canonical ontology.

## Directional boundary

```text
Enterprise Relation Representation
          ↓
       Adapter
          ↓
 Predicate Mapping Decision
          ↓
Existing Canonical Predicate
```

The mapping is directional. An enterprise relation MUST NOT create or redefine a canonical predicate merely because the source system exposes that relation.

## Mapping record

Each predicate mapping MUST preserve at least:

- `source_system`
- `source_entity_type`
- `source_entity_id`
- `source_relation_type`
- `source_target_entity_type`
- `source_target_entity_id`
- `canonical_predicate` when mapped
- `mapping_status`
- `mapping_confidence`
- `provenance`
- `canonical_mutation=false`

## Mapping status

- `mapped`: the source relation is sufficiently evidenced as equivalent to an existing canonical predicate.
- `ambiguous`: multiple canonical predicates remain plausible; no canonical relation fact is asserted.
- `unmappable`: no justified existing canonical predicate is available.
- `rejected`: the relation is intentionally excluded, such as a UI/workflow/control relation or vendor-only classification.

## Predicate semantics are not field names

A source relation such as `supplied_by`, `source_vendor`, `preferred_supplier`, `plant_vendor`, or `route_to` MUST NOT be treated as semantically equivalent solely because its name resembles a canonical predicate. Direction, endpoint types, cardinality, temporal scope, and business meaning must be evidenced.

## Endpoint integrity

A predicate mapping MUST NOT silently change the identity or type of either endpoint. Enterprise identifiers remain source representation and provenance. Mapping a relation does not itself create canonical entities.

## Cardinality and direction

Source cardinality and direction MAY be normalized only when the target canonical predicate explicitly supports the transformation. A reverse relation MUST NOT be inferred merely because a canonical inverse appears convenient.

## Provenance and confidence

`mapping_confidence` expresses confidence in the semantic correspondence between the enterprise relation and the selected canonical predicate. It MUST NOT be interpreted as confidence that the relationship is true, current, complete, or authoritative.

Provenance MUST identify the source representation from which the mapping decision was made.

## Semantic gaps

Ambiguous and unmappable relations MUST be classified as semantic gaps. The adapter MUST NOT create a new canonical predicate automatically to accommodate an enterprise relation.

## Canonical graph safety

Predicate mapping is read-only with respect to canonical ontology structure and graph semantics. S258 MUST NOT:

- create canonical predicates;
- redefine canonical predicates;
- create canonical entities as a mapping side effect;
- mutate canonical facts;
- infer relationship facts from mapping confidence alone.

In particular, predicate mapping establishes a mapping decision, not a canonical relationship fact.

## Non-goals

S258 does not define vendor connectors, automatic ontology learning, graph mutation, relationship fact ingestion, or enterprise transaction processing.
