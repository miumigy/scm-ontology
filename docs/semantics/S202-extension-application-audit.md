# S202 — Extension Application Audit

S202 records the governed application event as an immutable audit artifact.

```text
Application
  ↓
ExtensionApplicationAudit
  ├─ proposal
  ├─ registry version before/after
  ├─ applied_at
  └─ actor
```

The audit record does not mutate the registry or graph. It provides provenance for a future application event.
