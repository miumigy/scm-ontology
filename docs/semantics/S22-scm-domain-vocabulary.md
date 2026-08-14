# S22 — SCM Domain Vocabulary Contract

## Purpose

S22 defines how SCM-specific concepts are introduced above the Core Semantic Baseline without expanding Core unnecessarily.

## Minimal contract

```text
DomainVocabularyEntry
├─ name
├─ definition
├─ core_primitive
└─ synonyms
```

Every canonical domain term must have an explicit definition and an explicit relationship to a Core primitive.

## Rules

1. A domain term does not become Core merely because it is common in SCM.
2. Synonyms are vocabulary mappings, not separate semantic concepts by default.
3. A source-system field name is not automatically a canonical domain term.
4. Domain definitions must state their semantic boundary and avoid implementation-specific meaning.
5. New relationships or constraints require their own semantic contract; they must not be hidden inside a vocabulary entry.
6. Conflicting definitions cannot be silently merged; they require explicit resolution or scoped variants.

## Examples

```text
Inventory  ──extends──> Entity
Shipment   ──extends──> Entity
Demand     ──extends──> Entity / MetricDefinition
Capacity   ──extends──> Entity / State
```

These examples illustrate extension points only. S22 does not canonize these terms or define their full SCM semantics.

## Non-goals

S22 does not define:

- Inventory semantics
- Shipment lifecycle
- Demand planning semantics
- Production semantics
- enterprise-specific terminology
- source-system mappings
- synonym equivalence beyond explicit vocabulary declarations
