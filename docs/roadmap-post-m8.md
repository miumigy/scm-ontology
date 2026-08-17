
## Current phase — SCM OS Runtime (Phase R1)

**Status: Active — S348**

S348 is the first **Runtime Integration** milestone. It binds the S333..S346
governed cognitive loop into a deterministic, in-memory, side-effect-free
Python API (`run_decision_loop`), so the canonical path runs end to end:

```text
observations -> ReasoningInput -> ReasoningOutput -> ValidatedDecisionProposal
    -> AuthorizedDecision -> ExecutionCommand
```

S348 reuses the existing governed contracts and introduces no new canonical
semantics. A deterministic `MockReasoningProvider` exercises the loop without
LLM, rule, or optimization backends.

### Phase R — SCM OS Runtime

- [x] S348 SCM Decision Runtime v0 (governed loop as one Python API);
- [ ] R2 deterministic / rule-based / LLM reasoning providers;
- [ ] R3 execution runtime (ExecutionCommand -> Dry Run -> ExecutionResult);
- [ ] R4 governance (audit trail, decision replay, provenance, policy,
      human approval, override, command lifecycle).

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


## Canonical Graph runtime (completed — Phase 3/4)

**Status: Completed — S332**

S311–S325 establish the governed Canonical Graph, temporal query, reasoning, evidence, projection, freshness, invalidation, and governed query runtime boundaries.

S326 adds the first **Phase 4 business-question vertical slice**, resolving inventory position from already-canonical inventory facts.

S327 resolves demand/supply gap over an explicit item/period/unit scope.

S328 derives supplier schedule delay from an exact canonical supplier/item/unit scope.

S329 propagates explicit upstream risk over declared multi-hop supply dependencies.

S330 compares explicit capacity and requirement facts by exact resource/unit scope and reports headroom, utilization, and feasibility.

S331 propagates explicit disruption observations over declared directed dependencies with bounded paths and traceable evidence/provenance.

S332 reconciles explicit plan, actual, and commitment facts by exact item/period/unit scope, reporting three deterministic variances while preserving evidence/provenance.

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

- [x] inventory position across heterogeneous systems;
- [x] demand/supply gap;
- [x] supplier delay impact;
- [x] multi-hop supply risk;
- [x] capacity constraints;
- [x] network disruption propagation;
- [x] plan/actual/commitment reconciliation.

### Phase 5 — SCM OS integration

Connect the semantic layer to planning, simulation, optimization, visualization, and operational workflows while preserving the M8 boundary between derived decisions and Canonical Truth.

## Selection principle

Do not optimize for the largest number of connectors. Optimize for the smallest reference implementation that demonstrates:

**heterogeneous source → governed canonicalization → canonical graph → business question → explainable answer → traceable evidence**.
