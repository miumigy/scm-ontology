# SCM Ontology / SCM OS Primary Launch Handoff

> **Purpose:** authoritative handoff for another LLM/agent taking over the project after completion of the reference implementation phases.

## Mission

SCM Ontology is a framework-independent Canonical Semantic Model for Supply Chain Management. It connects heterogeneous enterprise evidence to Canonical Facts, Canonical Graphs, reasoning, projections, and a governed SCM OS without allowing source-system semantics to silently become truth.

The long-term target is a governed operating layer:

```text
Enterprise Evidence → Governed Canonicalization → Canonical Graph / State
→ Business Question → Explainable Reasoning → Simulation / Optimization
→ Authorization / Governance → Execution → Outcome → Canonical Event → Next Decision
```

## Current status

The major reference-runtime development sequence is complete through Phase 10:

- Semantic foundation / M8: complete
- SCM OS Runtime R1–R5: complete through S366
- Phase 6 Control Plane: complete
- Phase 7 Real Data Plane: complete
- Phase 8 Persistent SCM Graph: complete
- Phase 9 Closed-Loop Execution: complete
- Phase 10 Autonomous SCM Control: complete

**Do not start another broad capability-building Phase before launch preparation.** The next objective is the Primary Launch / Release Candidate.

## Non-negotiable invariants

1. **Canonical Truth is governed.** Mapping, inference, projection, reasoning, simulation, optimization, replay, and ingestion do not silently mutate Canonical Truth.
2. **Canonical Truth is distinct from derived truth.** Inference, confidence, aggregation, projections, and recommendations remain distinguishable from Canonical Facts.
3. **Evidence and provenance survive.** Governed outcomes remain traceable to source evidence and semantic scope.
4. **History survives.** Fact versions, lifecycle transitions, conflicts, resolutions, projections, invalidations, commands, outcomes, and agent steps remain reconstructable.
5. **Uncertainty survives.** Unknown, unresolved, stale, partial, disputed, failed, unsupported, and conflicted states remain observable.
6. **Replay is first-class.** Governed decisions, execution, and agent reasoning remain replayable without rewriting history.
7. **Scope is explicit.** Enterprise, tenant, organization, product, time, and other scopes never expand implicitly.
8. **Vendor semantics remain outside the Canonical Ontology** unless explicitly governed and versioned.
9. **AI is not the SCM OS.** AI/agents are reasoning or proposal providers. The OS owns state, governance, authorization, execution boundaries, and audit.
10. **External side effects are explicit.** Dry-run and real execution are distinct, and real execution passes through a governed injected adapter boundary.

## What is already built

```text
Canonical Ontology → Canonical Graph → Business Questions → Decision Runtime
→ Rule / LLM Reasoning → Proposal Validation → Authorization Governance
→ Execution Runtime → Audit / Command Lifecycle → SCM Applications
→ Simulation / Optimization → Operational Workflow → SCM OS Control Plane
→ Reference Data Plane → Persistent Graph → Closed-Loop Execution
→ Bounded Autonomous Control
```

Reference applications cover replenishment, procurement, production, and distribution. Multi-period simulation and deterministic planning/optimization are available. The Control Plane provides a coherent reference surface. Real-data adapters, relational/Neo4j persistence, closed-loop execution, and bounded agent autonomy have reference implementations and acceptance coverage.

## Critical interpretation of completion

Phase 10 completion means the **reference architecture and deterministic reference runtime are demonstrated**. It does **not** claim that the project is already a production enterprise SaaS, a universal ERP/WMS/TMS connector suite, or an unrestricted autonomous execution system.

Primary-launch non-claims:

- no universal SAP/WMS/TMS/APS connector claim;
- no production HA/SLA claim unless separately implemented and tested;
- no implicit multi-tenancy/security certification claim;
- no claim that inferred facts automatically become Canonical Truth;
- no claim of unrestricted autonomous execution.

Explicit production boundaries increase credibility.

## Primary Launch objective

Optimize for:

> **5-minute understanding, 10-minute execution, 30-minute extension.**

Demonstrate one complete Golden Path rather than expose every internal milestone.

### Recommended Golden Path

```text
Load reference SCM graph
→ Ask a supply-chain question
→ Detect / inspect an exception
→ Generate governed decision
→ Inspect evidence + rationale
→ Simulate / optimize alternative
→ Authorize
→ Execute dry-run
→ Inspect operational workflow
→ Inspect audit / replay
→ Agent proposes a bounded alternative
```

This is the primary launch acceptance story.

## Primary Launch workstreams

### L1 — Release Surface

Create a clean public-facing explanation of what SCM Ontology is, what SCM OS is, why Canonical Truth is governed, the architecture, reference workflow, current capabilities, explicit non-goals, quick start, and contribution path.

### L2 — Golden Path

Create one executable, deterministic end-to-end example. It must be runnable by a fresh clone and exercise the important existing boundaries without duplicating business logic.

Recommended location: `examples/primary_launch/` or an equivalent existing example structure. Provide a one-command entry point where practical.

### L3 — Packaging / Developer Experience

A fresh user should be able to install and run the reference scenario with minimal friction. Validate package metadata, imports, example dependencies, documentation links, and CI from a clean environment.

Prefer an entry point such as:

```bash
python -m scm_ontology.examples.primary_launch
```

or an equivalent documented command.

### L4 — Production Boundary Documentation

Document exactly what is reference-quality and what remains outside the primary-launch claim. Do not imply production enterprise connectors, security certification, deployment guarantees, SLA, or unrestricted autonomy without evidence.

### L5 — Primary Launch Acceptance

Create a compact launch checklist covering architecture coherence, clean installation, Golden Path execution, Canonical Truth boundary, provenance/evidence, governance and authorization, execution safety, agent safety, replay/audit, documentation, and CI.

## Development-history cleanup

The project has accumulated internal identifiers such as `Sxxx`, `Mxx`, `R1–R5`, `P6-A`, `P7-A`, `P8-A`, `P9-A`, and `P10-A`. These are useful engineering history but should not dominate the primary launch surface.

Recommended policy:

- **Do not delete Git history.**
- Preserve detailed milestone documents for traceability.
- Move or index historical milestone documents under `docs/history/` where appropriate.
- Keep the current README focused on product, architecture, and current capabilities rather than the complete sequence of internal slices.
- Treat Sxxx/Mxx/Px-x identifiers as historical development references after the launch cut.
- Introduce release-oriented identifiers such as `SCM Ontology v0.1` and `SCM OS Reference v0.1` instead of creating an endless S-number sequence.

This is an archive/refactoring activity, not a semantic rewrite.

## Suggested information architecture

```text
README.md
AGENTS.md
BACKLOG.yaml
registry/
src/
tests/
examples/

docs/
├── README.md
├── architecture/
├── semantics/
├── milestones/          # historical acceptance contracts
├── history/             # optional consolidated development history
├── launch/
│   ├── primary-launch.md
│   ├── golden-path.md
│   └── acceptance.md
└── reference/
```

Avoid moving large numbers of files solely for cosmetic reasons. Establish a clean current-vs-history boundary first.

## Agent takeover protocol

Any LLM agent continuing this project MUST first:

1. inspect the current `main` branch;
2. read `AGENTS.md`;
3. read `README.md` and `docs/README.md`;
4. inspect the current architecture and launch documents;
5. run the existing test suite before changing code;
6. search for an existing contract/function before introducing a new abstraction;
7. preserve the Canonical Truth / provenance / governance invariants;
8. avoid creating a new Phase or Sxxx task unless a genuine post-launch capability gap is demonstrated;
9. prefer a bounded launch slice with an E2E acceptance test over another isolated contract;
10. keep changes small, reviewable, deterministic, and documented.

When uncertain whether a new feature is needed, ask:

> **Does this materially improve the Golden Path, release surface, installability, safety, or evidence for the primary launch?**

If not, defer it to post-launch.

## Post-launch direction

After the primary launch, development can resume as product/platform evolution:

```text
SCM Ontology
   │
   ├── Reference Runtime
   ├── SCM OS
   ├── Enterprise Adapters
   │    ├── ERP
   │    ├── WMS
   │    ├── TMS
   │    └── APS / Planning
   ├── SCM Applications
   └── Governed Agents
```

Potential post-launch themes include real enterprise integration, multi-tenant deployment, enterprise IAM, operational observability, performance/scale, richer SCM applications, and increasingly capable but policy-bounded agents. These should not block the first credible OSS/reference release.

## Definition of done for the current chapter

```text
Reference Architecture       ✅
Semantic Governance          ✅
Decision Runtime             ✅
Execution Boundary           ✅
Control Plane                ✅
Real Data Reference Plane    ✅
Persistent Graph             ✅
Closed Loop                  ✅
Bounded Autonomous Control   ✅

Primary Launch Surface       ⬜
Golden Path                  ⬜
Packaging / DX               ⬜
Production Boundary Docs     ⬜
Launch Acceptance            ⬜
Release Candidate            ⬜
```

The next agent should therefore work **toward the release candidate, not toward another abstract Phase**.

## First post-handoff action

Create a launch-preparation PR that:

1. adds or updates the executable Golden Path;
2. adds a concise primary-launch acceptance test;
3. updates the README current-status section to emphasize the completed reference architecture and explicit production boundary;
4. adds a launch documentation index;
5. leaves historical S/M/P numbering intact in history documents but removes it from the main narrative where it is no longer useful.

Do not start new enterprise connectors or unrestricted agent autonomy as part of this first launch-preparation PR.
