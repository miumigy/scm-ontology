# S186 — Extension Candidate Queue

S186 adds a read-only projection for relations classified as `EXTENSION_CANDIDATE`.

```text
Validation Results
      ↓
extension_candidate_queue()
      ↓
Extension Candidates
```

The queue preserves source order and does not promote candidates into ontology definitions. Candidate review and eventual extension remain explicit downstream operations.
