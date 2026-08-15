# S225 — Path Consistency

S225 validates that a relation path remains a faithful projection of canonical graph identities.

Invariants:

- node count is relationship count + 1
- every relationship identity resolves in the canonical graph
- relationship endpoints are continuous with adjacent path nodes
- a relationship identity is not repeated within one path

```text
CanonicalGraph
    ↓
RelationPathMatch
    ↓
Path Consistency Gate
    ↓
Path Reasoning
```

The validator is read-only. It rejects malformed paths rather than repairing or inferring them.
