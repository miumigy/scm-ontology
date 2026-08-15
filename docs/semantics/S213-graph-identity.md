# S213 — Graph Identity

S213 fixes the graph node identity rule for canonical entities.

```text
CanonicalEntity
  entity_id + concept_ref
        ↓
GraphNodeIdentity
  node_id + node_type
```

`entity_id` is preserved as the graph `node_id`; `concept_ref` is preserved as the graph `node_type`. Attributes are deliberately excluded from identity so source attributes cannot silently create identity drift.

The rule is deterministic and read-only.
