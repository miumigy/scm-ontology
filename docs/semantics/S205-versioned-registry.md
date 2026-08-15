# S205 — Versioned Registry

S205 introduces immutable registry snapshots with explicit parent lineage.

```text
v1
 ↓ parent
v2
 ↓ parent
v3
```

Each snapshot has a unique version reference and content reference. A new snapshot must identify the current snapshot as its parent. Rollback is represented by selecting an existing snapshot; mutation remains outside this artifact.
