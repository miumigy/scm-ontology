# S229 — Reasoning Policy Boundary

S229 establishes an explicit policy boundary between canonical truth, derived information, and inference.

```text
CANONICAL  → authoritative semantic truth
DERIVED    → deterministic computation from canonical data
INFERRED   → reasoning output requiring explicit policy
```

Default policy:

- inferred facts are not enabled
- graph mutation is not enabled
- inferred facts cannot be promoted to canonical truth

Reasoning therefore remains read-only and evidence-bound unless an explicit policy opts into a stronger capability.
