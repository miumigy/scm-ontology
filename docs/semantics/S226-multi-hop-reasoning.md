# S226 — Multi-hop Reasoning

S226 composes the existing path query, path constraint, and path provenance layers into one read-only reasoning operation.

```text
RelationPathQuery
      ↓
Path Constraint
      ↓
PathEvidence
      ↓
PathReasoningResult
```

The operation does not add inferred edges or facts. It only composes existing canonical graph traversal with explicit constraints and provenance.

This is the first end-to-end multi-hop reasoning slice in the ontology runtime.
