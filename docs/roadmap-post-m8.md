
## Current phase — SCM OS Runtime (Phase R1–R5)

**Status: Active — S358**

S348 is the first **Runtime Integration** milestone. It binds the S333..S346
governed cognitive loop into a deterministic, in-memory, side-effect-free
Python API (`run_decision_loop`), so the canonical path runs end to end:

```text
observations -> ReasoningInput -> ReasoningOutput -> ValidatedDecisionProposal
    -> AuthorizedDecision -> ExecutionCommand
```

S348 reuses the existing governed contracts and introduces no new canonical
semantics. A deterministic `MockReasoningProvider` exercises the loop without
LLM, rule, or optimization backends. S351 adds a deterministic rule-based
provider, and S352 connects an injected, transport-neutral LLM client to the
same S368 boundary without coupling the ontology to a vendor SDK.

S353 adds the first Execution Runtime milestone: an immutable
`ExecutionCommand` is processed through a bounded, injected `ExecutionAdapter`
as a deterministic, side-effect-free dry run, producing a
`DryRunExecutionResult`.

S354 records a governed decision as a content-addressed audit entry and
replays the deterministic governed chain. S355 tracks the command lifecycle as
an immutable, governed state machine. S356 applies the fail-closed
authorization policy, human-approval, and senior-override gates. Together
S354–S356 form Phase R4 (Governance).

S358 is the first Phase R5 application: it resolves on-hand inventory
into a replenishment decision and, when a reorder is needed, drives it through
the governed loop to an authorized execution command and dry run. S360 resolves a demand/supply shortage into a procurement decision through the governed loop, and S361 resolves a production requirement against capacity into a scheduling decision. S358–S361 form the first Phase R5 application set.

### Phase R — SCM OS Runtime

- [x] S348 SCM Decision Runtime v0 (governed loop as one Python API);
- [x] S351 rule-based reasoning provider;
- [x] S352 LLM reasoning provider (injected, transport-neutral);
- [x] S353 execution runtime (ExecutionCommand -> Dry Run -> ExecutionResult);
- [x] S354 governed audit trail & decision replay;
- [x] S355 command lifecycle;
- [x] S356 authorization policy, approval & override;
- [x] S358 replenishment decision application;
- [x] S360 procurement decision application;
- [x] S361 production decision application;

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
