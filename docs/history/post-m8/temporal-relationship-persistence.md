# S314 — Relationship and Temporal Persistence

S314 extends the concrete graph-store boundary from canonical nodes to canonical relationships and their temporal semantic versions.

## Transport contract

`CanonicalGraph.to_mapping()` already represents a relationship as stable identity (`id`), endpoints (`from`, `to`), predicate, and optional version records. The Neo4j adapter transports that structure without changing its semantic meaning.

Temporal versions remain properties of the canonical relationship. They are not collapsed into a single current edge, so historical validity is preserved at the semantic boundary.

## Guardrails

- authorization still comes from S311/S312
- no identity resolution is performed
- no fuzzy matching is performed
- the ontology remains independent of the Neo4j driver
- temporal values are transported, not interpreted by the adapter

The next slice should address production transaction semantics and temporal query/read behavior rather than adding more persistence-specific ontology logic.
