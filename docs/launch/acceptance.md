# Primary Launch Acceptance (L5)

The L5 launch checklist is folded into one deterministic, content-addressed report by `src/scm_ontology.primary_launch_acceptance.py`.

## Running the acceptance

```bash
PYTHONPATH=src python -m scm_ontology.primary_launch_acceptance --self-check
```

Print the full report as JSON:

```bash
PYTHONPATH=src python -m scm_ontology.primary_launch_acceptance --json
```

## Checklist items

1. **Architecture coherence** — the control-plane E2E traverses all governed stages.
2. **Clean installation** — the core modules import cleanly.
3. **Golden Path execution** — `run_primary_launch` is accepted.
4. **Reference data demonstration** — ERP + WMS + TMS convergence is deterministic and reference-only.
5. **Canonical Truth boundary** — derived/reference state stays derived; no canonical mutation.
6. **Provenance and evidence** — results are content-addressed and evidence-bound.
7. **Governance and authorization** — authorization is mandatory and fails closed.
8. **Execution safety** — execution is bounded, in-memory, side-effect-free.
9. **Agent safety** — proposals are validated; bounded actions only.
10. **Replay and audit** — deterministic, content-addressed, auditable.
11. **Launch documentation** — launch index, Golden Path, demo, acceptance, release checklist, release notes, and limitations exist.
12. **Release package** — `CHANGELOG.md`, `CONTRIBUTING.md`, `LICENSE`, and package version `0.1.0` are present.
13. **CI entry** — the validator, Golden Path, acceptance, full tests, and installed-package Golden Path are part of CI.

## Acceptance rule

The launch is accepted only when **every** checklist item is operable. Any probe that errors or returns an unusable result fails closed.

## Release rule

A green L5 acceptance establishes **source-tree release readiness**. The final `v0.1.0` Git tag/GitHub Release is created only after the release commit has been merged and CI remains green.
