# Golden Path

The primary-launch acceptance story is one executable Golden Path optimized for **5-minute understanding, 10-minute execution, 30-minute extension**.

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

Print the full result as JSON:

```bash
PYTHONPATH=src python -m scm_ontology.primary_launch --json
```

Then run the concrete multi-source reference demo:

```bash
PYTHONPATH=src python examples/primary_launch_demo.py
```

The demo is deliberately separate from the SCM OS cognitive loop: it makes the data-plane semantic boundary visible before the decision loop is exercised.

## What the demo proves

The ERP + WMS + TMS reference path demonstrates:

1. heterogeneous source representations;
2. source-specific quality gates;
3. explicit source-to-model mapping;
4. explicit identity resolution using a shared signal;
5. a deterministic, content-addressed reference graph;
6. source members and evidence/provenance remaining attached;
7. relationships resolving to converged nodes;
8. a `reference` boundary rather than an implicit Canonical Truth mutation.

## Implementation

- `src/scm_ontology/primary_launch.py` — `run_primary_launch(...)` and the module entry point.
- `src/scm_ontology/primary_launch_acceptance.py` — machine-executable L5 gate.
- `src/scm_ontology/multi_source_reference.py` — deterministic ERP/WMS/TMS-shaped reference convergence.
- `examples/primary_launch_demo.py` — human-readable presentation of the reference graph.
- Each Golden-Path step is recorded as an immutable `GoldenPathStep`; the launch is accepted only when every governed step succeeds.
