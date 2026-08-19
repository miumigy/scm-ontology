# Golden Path

The primary-launch acceptance story is one executable Golden Path optimized
for **5-minute understanding, 10-minute execution, 30-minute extension**.

## The path

```text
Load reference SCM graph
-> Ask a supply-chain question
-> Detect / inspect an exception
-> Generate governed decision
-> Inspect evidence + rationale
-> Simulate / optimize alternative
-> Authorize
-> Execute dry-run
-> Inspect operational workflow
-> Inspect audit / replay
-> Agent proposes a bounded alternative
```

## Running it

```bash
PYTHONPATH=src python -m scm_ontology.primary_launch --self-check
```

This composes the existing governed reference runtime — the control-plane
E2E and the closed-loop E2E — into one deterministic, content-addressed
result. It performs **no external side effects** and never mutates Canonical
Truth.

Print the full result as JSON:

```bash
PYTHONPATH=src python -m scm_ontology.primary_launch --json
```

## Implementation

- `src/scm_ontology/primary_launch.py` — `run_primary_launch(...)` and the
  module entry point.
- Each Golden-Path step is recorded as an immutable `GoldenPathStep`; the
  launch is accepted only when every governed step succeeds.
