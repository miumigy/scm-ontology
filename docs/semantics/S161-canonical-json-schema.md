# S161 — Canonical JSON Schema

S161 publishes the first machine-validation contract for the Canonical Assertion Model.

## Boundary

```text
Semantic Model
      ↓
Canonical Assertion Model
      ↓
Serialization Boundary
      ↓
Canonical JSON Schema
      ↓
Machine Validation
```

The schema validates the serialized assertion envelope. It is an interchange contract, not the ontology itself.

## Design rules

- Assertion identity is explicit.
- Entity-value and relation assertions share the same context envelope.
- Temporal, epistemic, and provenance context remain explicit.
- Additional storage or graph semantics are not introduced.
- Cross-object invariants that JSON Schema cannot express remain runtime validation responsibilities.

## Non-goals

No RDF vocabulary, graph schema, persistence model, inference rules, or enterprise mapping is defined here.
