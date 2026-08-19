# Primary Launch Acceptance (L5)

The L5 launch checklist is folded into one deterministic, content-addressed
report by `src/scm_ontology/primary_launch_acceptance.py`.

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
4. **Canonical Truth boundary** — derived state stays derived; no canonical mutation.
5. **Provenance and evidence** — results are content-addressed and evidence-bound.
6. **Governance and authorization** — authorization is mandatory and fails closed.
7. **Execution safety** — execution is bounded, in-memory, side-effect-free.
8. **Agent safety** — proposals are validated; bounded actions only.
9. **Replay and audit** — deterministic, content-addressed, auditable.
10. **Launch documentation** — launch index + primary-launch + golden-path + acceptance exist.
11. **CI entry** — the self-check command is documented in the README.

## Acceptance rule

The launch is accepted only when **every** checklist item is operable. Any
probe that errors or returns an unusable result fails closed.
