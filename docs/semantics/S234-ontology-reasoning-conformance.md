# S234 — Ontology / Reasoning Conformance

S234 defines the conformance gate between the canonical ontology boundary and reasoning results.

The gate verifies two properties:

- a reasoning result is safe to keep outside canonical truth
- the default reasoning policy remains read-only

```text
Canonical Ontology Boundary
          ↓
   Reasoning Result
          ↓
 Conformance Gate
          ↓
 Canonical-safe / Policy-safe
```

Conformance does not promote inferred information, mutate the graph, or reinterpret ontology semantics.
