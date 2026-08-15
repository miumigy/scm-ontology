# S201 — Registry Transaction Boundary

S201 introduces an immutable transaction artifact for canonical registry transitions.

```text
validated registry
      ↓
prepare(before, after)
      ↓
RegistryTransaction
      ↓
commit() → after snapshot
```

The transaction is atomic at the semantic model boundary: it represents one complete snapshot transition. No partial external mutation is performed by the transaction object itself.
