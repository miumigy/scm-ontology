# S204 — Extension Rollback / Rejection

S204 models non-successful application outcomes without performing destructive rollback.

```text
Application
   ├─ applied
   ├─ rejected ── reason_ref
   └─ rolled_back ── reason_ref + transaction_ref
```

Rejection means the application never crossed the committed mutation state. Rollback means a previously applied transaction was subsequently reverted. The outcome model is immutable and does not itself mutate the registry.
