# Primary Launch — Release Surface & Production Boundary

> **SCM Ontology v0.1** / **SCM OS Reference v0.1**

## What is being released

A framework-independent **Canonical Semantic Model** for Supply Chain
Management, together with a governed **reference runtime** (SCM OS Reference)
that demonstrates the full cognitive loop:

```text
Enterprise Evidence -> Governed Canonicalization -> Canonical Graph / State
-> Business Question -> Explainable Reasoning -> Simulation / Optimization
-> Authorization / Governance -> Execution -> Outcome -> Canonical Event
-> Next Decision
```

The reference runtime covers observation, decision context assembly, rule and
LLM reasoning providers, proposal validation, authorization/governance,
execution (dry-run, in-memory), operational workflow, audit/replay, persistent
graph backends (relational and Neo4j), closed-loop execution, reference data
adapters, and bounded autonomous control.

## Explicit production boundaries (non-claims)

The primary-launch release does **not** claim:

- a universal SAP / WMS / TMS / APS connector suite;
- production-grade high availability or a formal SLA;
- multi-tenant / enterprise-IAM / security certification;
- that inferred or projected facts automatically become Canonical Truth;
- unrestricted autonomous execution.

Explicit boundaries increase credibility. Real enterprise integration,
multi-tenant deployment, enterprise IAM, operational observability,
performance/scale, and richer SCM applications are post-launch themes.

## Release surface

- **CLI Golden Path:** `PYTHONPATH=src python -m scm_ontology.primary_launch --self-check`
- **Acceptance:** `PYTHONPATH=src python -m scm_ontology.primary_launch_acceptance --self-check`
- **Contract validation:** `PYTHONPATH=src python -m scm_ontology.validator`

See [`golden-path.md`](golden-path.md) for the executable story and
[`acceptance.md`](acceptance.md) for the L5 checklist.
