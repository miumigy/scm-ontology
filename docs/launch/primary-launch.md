# Primary Launch — Release Surface & Production Boundary

> **SCM Ontology v0.1.0** / **SCM OS Reference v0.1.0**

## What is being released

A framework-independent **Canonical Semantic Model** for Supply Chain Management, together with a governed **reference runtime** (SCM OS Reference) that demonstrates the full cognitive loop:

```text
Enterprise Evidence -> Governed Canonicalization -> Canonical Graph / State
-> Business Question -> Explainable Reasoning -> Simulation / Optimization
-> Authorization / Governance -> Execution -> Outcome -> Canonical Event
-> Next Decision
```

The reference runtime covers observation, decision context assembly, rule and LLM reasoning providers, proposal validation, authorization/governance, bounded execution, operational workflow, audit/replay, persistent graph backends, closed-loop execution, reference data adapters, and bounded autonomous control.

## Primary Launch experience

The public surface is optimized for:

> **5-minute understanding, 10-minute execution, 30-minute extension.**

Use the Golden Path first, then the multi-source demo:

```bash
PYTHONPATH=src python -m scm_ontology.primary_launch --self-check
PYTHONPATH=src python examples/primary_launch_demo.py
```

The demo uses ERP + WMS + TMS-shaped reference inputs, converges heterogeneous records through explicit quality/mapping/identity boundaries, and produces a deterministic reference graph. It has no external side effects.

## Explicit production boundaries (non-claims)

The primary-launch release does **not** claim:

- a universal SAP / WMS / TMS / APS connector suite;
- production-grade high availability or a formal SLA;
- multi-tenant / enterprise-IAM / security certification;
- that inferred or projected facts automatically become Canonical Truth;
- unrestricted autonomous execution;
- production-scale graph performance, disaster recovery, or managed-service guarantees;
- replacement of APS, optimizer, scheduler, or planning suites.

See [`limitations.md`](limitations.md) for the authoritative boundary list.

## Release surface

- **Contract validation:** `PYTHONPATH=src python -m scm_ontology.validator`
- **Golden Path:** `PYTHONPATH=src python -m scm_ontology.primary_launch --self-check`
- **L5 acceptance:** `PYTHONPATH=src python -m scm_ontology.primary_launch_acceptance --self-check`
- **Full tests:** `PYTHONPATH=src pytest -q`
- **Multi-source demo:** `PYTHONPATH=src python examples/primary_launch_demo.py`

See [`golden-path.md`](golden-path.md), [`demo.md`](demo.md), and [`acceptance.md`](acceptance.md).

## Release package

- [`release-checklist.md`](release-checklist.md)
- [`release-notes-v0.1.0.md`](release-notes-v0.1.0.md)
- [`../../CHANGELOG.md`](../../CHANGELOG.md)
- [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md)
- [`limitations.md`](limitations.md)

The source tree is release-ready when CI is green and the release checklist is satisfied. The final repository publication step is the `v0.1.0` tag/GitHub Release after the merge commit is stable.
