# Primary Launch — SCM Ontology v0.1.0 / SCM OS Reference v0.1.0

This directory is the **public launch surface**. It is intentionally much smaller than the historical engineering record.

## Start here

1. [`primary-launch.md`](primary-launch.md) — what is released and what is not claimed.
2. [`golden-path.md`](golden-path.md) — one executable end-to-end story.
3. [`demo.md`](demo.md) — a concrete multi-source ERP + WMS + TMS example.
4. [`acceptance.md`](acceptance.md) — the machine-executable L5 launch gate.
5. [`release-checklist.md`](release-checklist.md) — final release readiness checklist.
6. [`limitations.md`](limitations.md) — explicit production boundaries.
7. [`release-notes-v0.1.0.md`](release-notes-v0.1.0.md) — v0.1.0 release notes.

The authoritative project handoff is [`../primary-launch-handoff.md`](../primary-launch-handoff.md).

## Public release identifiers

- **SCM Ontology v0.1.0**
- **SCM OS Reference v0.1.0**

`Sxxx`, `Mxx`, and `Px-x` identifiers remain in historical engineering documents for traceability. They are no longer the active public planning mechanism.

## Launch commands

```bash
PYTHONPATH=src python -m scm_ontology.validator
PYTHONPATH=src python -m scm_ontology.primary_launch --self-check
PYTHONPATH=src python -m scm_ontology.primary_launch_acceptance --self-check
PYTHONPATH=src pytest -q
python -m examples.primary_launch_demo
```

The CI workflow runs the validator, Golden Path, L5 acceptance, full tests, package installation, and an installed-package Golden Path check.
