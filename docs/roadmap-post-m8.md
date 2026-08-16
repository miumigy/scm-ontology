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

**Status: Active — S320**

The post-M8 implementation has progressed from machine-readable vocabulary and explicit reference canonicalization into a governed graph runtime. S311–S314 establish persistence planning, transport adapters, the Neo4j boundary, and temporal relationship persistence. S317 provides temporal semantic path traversal, S318 evaluates those paths against explicit constraints, and S319 provides the stable read-only temporal query surface.

S320 adds the first explicit **what-if scenario boundary**. A scenario is an immutable set of declared hypothetical relationship operations evaluated against a derived graph view; it never mutates Canonical Truth.

```mermaid
flowchart LR
    CG[Canonical Graph] --> T[Temporal versions]
    T --> Q[S319 Temporal Query]
    Q --> SC[S320 Scenario Overlay]
    SC --> V[Derived hypothetical graph]
    V --> Q2[Temporal Query]
    Q2 --> R[Scenario result + base/scenario provenance]
    SC -. no Canonical Truth mutation .-> CG
```

The scenario surface is deliberately conservative. It supports explicit `add`, `remove`, and `replace` relationship operations only. It does not perform identity resolution, fuzzy matching, inference, optimization, allocation, feasibility optimization, or execution. This makes it suitable as a semantic input boundary for future planning and simulation systems.

### Phase 1 — Reference semantic implementation

- [x] machine-readable canonical entity / predicate / relationship registry;
- [x] stable concept references and relationship signatures;
- [x] registry uniqueness and endpoint validation;
- [x] Python registry ↔ machine-readable registry drift detection;
- [x] versioned schema validation for the registry artifact;
- [ ] documentation generated from canonical metadata where practical.

### Phase 2 — Enterprise canonicalization

- [x] realistic ERP/WMS/TMS/APS fixtures;
- [x] explicit source mappings;
- [x] ambiguity and Semantic Gap handling;
- [x] provenance and evidence preservation;
- [ ] governed identity resolution;
- [ ] controlled application into Canonical Fact Versions.

### Phase 3 — Canonical Graph runtime

- [x] governed graph persistence planning;
- [x] transport-neutral graph-store adapter;
- [x] optional injected Neo4j adapter;
- [x] temporal relationship persistence;
- [x] temporal semantic path traversal;
- [x] constraint-aware feasibility reasoning;
- [x] deterministic temporal semantic query boundary;
- [x] immutable scenario overlay boundary;
- [ ] evidence-aware traversal;
- [ ] projection and materialization runtime.

### Phase 4 — SCM value applications

Prioritize questions that demonstrate why a canonical SCM semantic layer matters:

- inventory position across heterogeneous systems;
- demand/supply gap;
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
