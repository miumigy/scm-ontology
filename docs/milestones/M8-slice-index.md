# M8 Slice Index

M8 is complete. This index provides a compact map from contract to architectural role.

| Slice | Architectural role |
|---|---|
| S294 | Conflict and Resolution governance |
| S300 | Canonical Fact lifecycle / versioning |
| S301 | Explicit Fact application boundary |
| S302 | Historical and temporal reconstruction |
| S303 | Canonical Graph read / projection boundary |
| S304 | Projection freshness / lineage |
| S305 | Governed projection querying |
| S306 | Projection materialization |
| S307 | Dependency invalidation / impact propagation |
| S308 | Cross-projection consistency / rebuild |
| S309 | Operational readiness / governance |
| S310 | End-to-end M8 acceptance / closure |

```mermaid
flowchart TB
    S294[Conflict / Resolution] --> S300[Fact Lifecycle]
    S300 --> S301[Application]
    S301 --> S302[Historical Query]
    S302 --> S303[Graph Read]
    S303 --> S304[Lineage / Freshness]
    S304 --> S305[Projection Query]
    S305 --> S306[Materialization]
    S306 --> S307[Invalidation]
    S307 --> S308[Consistency / Rebuild]
    S308 --> S309[Operations]
    S309 --> S310[Acceptance]
```

The contracts are cumulative. A later slice does not supersede a safety invariant from an earlier slice; it composes with it.
