# S160 — Canonical Serialization Boundary

S160 defines the first machine-readable export boundary for the Canonical Assertion Model.

## Architecture

```text
Canonical Assertion Model
          ↓
  Serialization Boundary
          ↓
JSON-compatible mapping
          ↓
JSON / JSON Schema / RDF / Graph adapters
```

The serializer emits a JSON-compatible mapping but does not make JSON the ontology itself.

## Principles

- Domain objects remain the source of semantic truth.
- Serialization must not change assertion semantics.
- Temporal, epistemic, and provenance context remain explicit.
- Source identifiers are not promoted to canonical identity.
- Storage-specific representations are outside the core model.

## Non-goals

S160 does not define JSON Schema, RDF vocabulary, graph database storage, versioning, or persistence.
