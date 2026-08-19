# SCM Ontology / SCM OS Primary Launch Handoff

> **Authoritative handoff for the public v0.1.0 release boundary.**

## Mission

SCM Ontology is a framework-independent semantic model for Supply Chain Management. It connects heterogeneous enterprise evidence to governed facts, graphs, reasoning, projections, and a governed SCM OS without allowing source-system semantics to silently become truth.

## Current release status

The reference-runtime development chapter is complete through Phase 10. The project is now **release-oriented**.

**Current target: SCM Ontology v0.1.0 / SCM OS Reference v0.1.0.**

The Primary Launch surface is complete:

- public README and Japanese README;
- executable Golden Path;
- deterministic ERP + WMS + TMS reference-data demo;
- L5 machine-executable acceptance gate;
- explicit production-boundary documentation;
- release checklist and release notes;
- `CHANGELOG.md`;
- `CONTRIBUTING.md`;
- MIT `LICENSE`;
- release-oriented `BACKLOG.yaml`.

## Golden Path

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

Run:

```bash
PYTHONPATH=src python -m scm_ontology.primary_launch --self-check
PYTHONPATH=src python examples/primary_launch_demo.py
PYTHONPATH=src python -m scm_ontology.primary_launch_acceptance --self-check
```

## Non-negotiable invariants

1. Governed facts are not silently mutated by mapping, inference, projection, ingestion, replay, or reasoning.
2. Derived/reference state remains distinguishable from governed facts.
3. Evidence, provenance, scope, temporal context, uncertainty, and history survive.
4. Authorization and external side effects remain explicit boundaries.
5. AI/agents are reasoning or proposal providers and cannot bypass governance.
6. Execution is bounded and auditable.

## Primary-launch non-claims

The release does not claim universal ERP/WMS/TMS/APS connectors, production HA/SLA, enterprise IAM/security certification, production-scale graph guarantees, unrestricted autonomy, or replacement of APS/optimizer/planning suites.

See [`docs/launch/limitations.md`](launch/limitations.md).

## Planning policy after v0.1.0

Do **not** create an endless new sequence of `Sxxx`, `Mxx`, or `Phase` identifiers. Those identifiers are historical engineering references only.

Post-launch work is tracked by public releases (`0.2.0`, `0.3.0`, …) and capability outcomes in [`BACKLOG.yaml`](../BACKLOG.yaml).

## Release gate

The source tree is release-ready when CI is green and [`docs/launch/release-checklist.md`](launch/release-checklist.md) is satisfied.

The final repository publication step is:

```text
merge release PR
→ verify green main CI
→ create Git tag v0.1.0
→ create GitHub Release
```

No further broad capability-building Phase should block the first public release.
