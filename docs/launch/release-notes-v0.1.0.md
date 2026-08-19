# SCM Ontology v0.1.0 / SCM OS Reference v0.1.0

## Release theme

**A governed, executable reference model for SCM semantics and an SCM OS control loop.**

This first public release is intentionally a reference implementation. Its value is the explicit semantic and governance boundary, not a claim to replace enterprise systems.

## Included

- Framework-independent SCM semantic model and machine-readable registry.
- Governed canonical graph and semantic query foundations.
- Evidence/provenance-aware projections and lifecycle controls.
- SCM OS decision, reasoning, authorization, execution, audit, and replay boundaries.
- Reference data adapters and a deterministic ERP + WMS + TMS multi-source convergence example.
- Relational and Neo4j reference graph backends.
- Closed-loop and bounded autonomous-control reference paths.
- One deterministic Primary Launch Golden Path.
- L5 Primary Launch acceptance as a machine-executable CI gate.
- Japanese and English public documentation.

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

## Explicit non-goals

See [`limitations.md`](limitations.md). In particular, this release does not claim universal enterprise connectors, production HA/SLA, enterprise security certification, unrestricted autonomous execution, or that derived data automatically becomes Canonical Truth.

## Validation

The release gate runs:

```bash
PYTHONPATH=src python -m scm_ontology.validator
PYTHONPATH=src python -m scm_ontology.primary_launch --self-check
PYTHONPATH=src python -m scm_ontology.primary_launch_acceptance --self-check
PYTHONPATH=src pytest -q
```

The CI workflow also installs the package and reruns the Golden Path without `PYTHONPATH`.

## Upgrade / compatibility note

`0.1.0` establishes the first release-oriented public boundary. Future changes should be evaluated against the semantic invariants and documented as releases rather than extending the historical S/M/Phase numbering indefinitely.
