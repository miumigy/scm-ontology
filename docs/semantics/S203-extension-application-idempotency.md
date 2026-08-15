# S203 — Extension Application Idempotency

S203 defines an application key from the proposal reference and target registry version.

```text
(proposal_ref, target_registry_version)
              ↓
       Application Key
              ↓
   already applied? → reject
```

The check is read-only. It does not mutate the registry or audit store.
