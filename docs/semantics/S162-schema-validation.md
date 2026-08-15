# S162 — Schema Validation / Round-trip Contract

S162 connects the runtime Canonical Assertion Model, its serialization boundary, and the published JSON Schema.

## Contract

```text
Canonical Assertion Model
        ↓
serialize_assertion_set()
        ↓
JSON-compatible payload
        ↓
canonical-assertion-set.schema.json
        ↓
Machine validation
```

The critical invariant is that the canonical runtime model can produce a payload accepted by its published schema.

## Validation responsibilities

### JSON Schema
- structure
- required fields
- primitive/container types
- envelope shape

### Runtime model
- assertion identity uniqueness
- subject/context consistency
- relation/context consistency
- semantic invariants not expressible safely in the schema

## Boundary

S162 does not introduce deserialization, persistence, graph storage, or reasoning. It establishes a regression contract between the model, serializer, and schema.
