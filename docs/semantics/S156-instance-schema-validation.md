# S156 — Core Instance Schema Validation

S156 validates the S155 instance layer against the canonical semantic registry.

## Contract

```text
Canonical Entity
   ├─ concept_ref ──→ Canonical Concept
   └─ attributes

Canonical Relation
   ├─ predicate_ref ─→ Canonical Relationship
   ├─ subject_id ────→ Canonical Entity
   └─ object_id ─────→ Canonical Entity
```

S155 guarantees structural referential integrity. S156 adds semantic referential integrity.

## Validation gates

- Entity concept references must resolve to the canonical concept registry.
- Relation predicates must resolve to the canonical relationship registry.
- Entity and relation endpoint resolution remains enforced by `CoreInstanceModel`.
- An ingestion adapter may supply an explicit concept mapping override, but the canonical entity `concept_ref` is authoritative by default.

## Architectural boundary

```text
Semantic Registry
      ↓
Core Schema
      ↓
Core Instance Model
      ↓
Instance Validation
      ↓
Graph / Mapping / Reasoning consumers
```

The validator does not infer missing concepts, perform fuzzy matching, or mutate instances. Enterprise identity resolution remains the responsibility of the S153 mapping layer.

## Non-goals

No database constraints, graph traversal, SHACL engine, OWL reasoner, or enterprise-specific mapping rules are introduced here.
