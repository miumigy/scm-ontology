# S216 — Semantic Constraint Evaluation

S216 adds the first explicit constraint-evaluation boundary after the reasoning query boundary.

```text
CanonicalGraph
     ↓
NodeQuery
     ↓
SemanticNode*
     ↓
PropertyEquals
     ↓
matching node identities
```

The initial constraint is deliberately narrow: equality against a canonical node property. It evaluates existing facts only; it does not derive new facts, mutate the graph, or modify ontology semantics.
