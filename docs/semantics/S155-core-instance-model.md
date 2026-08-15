# S155 — Canonical Core Instance Model

S155 introduces the minimal instance layer beneath the semantic schema.

## Model

```text
Canonical Concept
      ↓ instantiates
Canonical Entity
      ↓ connected by
Canonical Relation
```

The model intentionally contains only:

- canonical entity identity
- concept reference
- attributes as values
- relation identity
- subject / predicate / object references
- optional relation qualifiers

## Invariants

1. Entity identifiers are unique within a model.
2. Relation identifiers are unique within a model.
3. Every relation subject resolves to an entity in the same model.
4. Every relation object resolves to an entity in the same model.
5. Source-system identifiers remain attributes or external resolution artifacts; they do not become canonical identity implicitly.

## Why this is a separate layer

`CanonicalGraph` already provides a graph-oriented transport representation. S155 instead defines the semantic instance contract that a graph adapter can consume.

```text
Semantic Schema
      ↓
Core Instance Model
      ↓
Graph / JSON / RDF / Database adapters
```

The ontology therefore does not depend on a particular graph database or serialization format.

## Non-goals

S155 does not define storage, graph traversal, source-system mappings, event sourcing, temporal versioning, or inference. Those are downstream capabilities that consume this instance contract.
