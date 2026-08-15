# S152 — Canonical Type / Attribute Semantics

S152 promotes the existing S114 type/value contract into a schema-facing contract without replacing the established vocabulary.

## Layers

```text
Concept
  ↓
Attribute Definition
  ↓
Canonical Type
  ↓
Value
```

An attribute identifies what a concept can carry; a type identifies what kind of value it can carry; a value is an instance of that type.

## Core boundaries

- Type ≠ Value
- Attribute ≠ Value
- Quantity ≠ bare number
- Reference ≠ identifier
- Cardinality ≠ nullability

Quantity types require explicit unit semantics. Reference types require an explicit target concept.

## Cardinality / nullability

Cardinality describes how many values may occur. Nullability describes whether a value may be absent within the allowed cardinality semantics. These are related but not interchangeable.

A mandatory `1` attribute cannot be nullable.

## Compatibility

S152 intentionally reuses S114's `ValueKind`, `Cardinality`, `ValueType`, and `AttributeDefinition` vocabulary. The new schema-facing objects provide stable references for later JSON Schema / RDF / OWL / graph adapters.

No vendor datatype or database column type is made canonical here.
