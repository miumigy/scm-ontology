# S217 — Evidence / Provenance

S217 defines a transport-neutral provenance model for facts consumed by reasoning.

```text
Observed Fact
    ↓
EvidenceRef
    ├─ source_ref
    ├─ observed_at
    └─ metadata
    ↓
EvidenceSet
```

Evidence provenance is kept separate from canonical entity identity and relation semantics. A source reference identifies evidence; it does not become the canonical entity identity.

This model records evidence only. It does not assert truth, infer new facts, or mutate the canonical graph.
