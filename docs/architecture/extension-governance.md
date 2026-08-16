# Extension Governance Architecture

S190–S209 established the governed extension lifecycle for SCM Ontology. This document remains a historical architecture contract and is compatible with the post-M8 governance model.

```mermaid
flowchart LR
    P[Proposal] --> D[Governance Decision]
    D --> AP[Application Plan]
    AP --> V[Validation / Gate / Preflight]
    V --> I[Intent / Mutation Guard]
    I --> M[Canonical Registry Mutation]
    M --> X[Integrity / Inverse Pairing]
    X --> T[Transaction Boundary]
    T --> A[Audit / Idempotency]
    A --> O[Outcome / Versioning]
    O --> S[Serialization / Graph Projection]
    S --> R[Reasoning Compatibility]
    R --> L[Extension Lifecycle]
```

## Architectural boundaries

- Governance decides whether an extension may proceed.
- Mutation changes canonical state only behind the mutation boundary.
- Integrity validation checks the resulting canonical registry.
- Versioning preserves immutable registry history.
- Serialization exposes a machine-readable representation.
- Graph projection is read-only and preserves canonical relation semantics.
- Reasoning compatibility validates the vocabulary before reasoning consumers use it.
- Lifecycle state records the governed status of an extension without performing mutation itself.

## Post-M8 interpretation

The extension lifecycle is one instance of the broader M8 principle: **semantic change is a governed operation, not an implicit side effect of parsing, inference, projection, or runtime convenience.** New implementations must also preserve provenance, historical lineage, explicit outcomes, replayability, and scope boundaries.
