# Post-M8 Implementation Roadmap

M8 completes the semantic and operational contract-definition phase. The next objective is to convert those contracts into a reference implementation and then into SCM business value.

```mermaid
flowchart LR
    A[M8 Contracts] --> B[Machine-Readable Registry]
    B --> C[Reference Canonicalization]
    C --> D[Realistic Multi-Source Fixtures]
    D --> E[Canonical Graph Runtime]
    E --> F[Governed Identity Resolution]
    F --> G[SCM Business Questions]
    G --> H[Planning / Simulation / SCM OS]
    H --> I[Production Operations]
```

## Current phase — Canonical Graph runtime

**Status: Active — S327**

The post-M8 implementation has progressed from machine-readable vocabulary and explicit reference canonicalization into a governed graph runtime. S311–S314 establish persistence planning, transport adapters, the Neo4j boundary, and temporal relationship persistence. S317 provides temporal semantic path traversal, S318 evaluates those paths against explicit constraints, S319 provides the stable read-only temporal query surface, S320 provides the immutable what-if scenario boundary, and S321 provides evidence-aware traversal.

S322 established the deterministic **projection/materialization runtime boundary**. A projection is derived state computed from Canonical Graph input; its source digest, projection identity, and projection version are preserved as lineage. Materialization never mutates Canonical Truth.

S323 adds the first **evidence-aware projection boundary**. Projection code can explicitly request governed evidence for a canonical relationship, and the runtime records only the evidence actually consulted. Missing required evidence fails closed; evidence remains derived provenance rather than Canonical Truth or authorization.

S324 adds a pure **projection freshness and invalidation runtime**. It classifies materialized projections as `current`, `stale`, `rebuild_required`, or `invalid` from explicit dependency and contract comparisons, while keeping persistence, scheduling, authorization, and governed recovery outside the semantic runtime.

S325 adds the **governed projection query boundary**. A query can expose a materialized projection only when its requested identity/version and contract are compatible and S324 reports `current`; stale, invalid, and rebuild-required projections fail closed with their lifecycle reason preserved.

S326 adds the first **Phase 4 business-question vertical slice**, resolving an inventory position (`available = on_hand + inbound - outbound`) from already-canonical inventory facts without identity resolution, allocation, or graph mutation.

S327 adds the second **Phase 4 business-question vertical slice**, resolving a demand/supply gap (`gap = max(demand - supply, 0)`) from already-canonical demand and supply facts over an explicit item/period/unit scope without allocation, optimization, or business-policy decisions.

### Phase 3 — Canonical Graph runtime

- [x] governed graph persistence planning;
- [x] transport-neutral graph-store adapter;
- [x] optional injected Neo4j adapter;
- [x] temporal relationship persistence;
- [x] temporal semantic path traversal;
- [x] constraint-aware feasibility reasoning;
- [x] deterministic temporal semantic query boundary;
- [x] immutable scenario overlay boundary;
- [x] evidence-aware traversal boundary;
- [x] projection/materialization reference runtime;
- [x] evidence-aware projections;
- [x] projection freshness and invalidation runtime;
- [x] governed projection query boundary.

### Phase 4 — SCM value applications

Prioritize questions that demonstrate why a canonical SCM semantic layer matters:

- [x] inventory position across heterogeneous systems;
- [x] demand/supply gap;
- supplier delay impact;
- multi-hop supply risk;
- capacity constraints;
- network disruption propagation;
- plan/actual/commitment reconciliation.

### Phase 5 — SCM OS integration

Connect the semantic layer to planning, simulation, optimization, visualization, and operational workflows while preserving the M8 boundary between derived decisions and Canonical Truth.

## Selection principle

Do not optimize for the largest number of connectors. Optimize for the smallest reference implementation that demonstrates:

**heterogeneous source → governed canonicalization → canonical graph → business question → explainable answer → traceable evidence**.
