# S343 — Reasoning Output Boundary

S343 defines the storage- and engine-neutral boundary for a reasoning engine's proposed decision result.

```text
S342 ReasoningInput
        ↓
Reasoning Engine
        ↓
S343 ReasoningOutput
        ↓
Future Decision Proposal / Governance
```

The output is explicitly a **proposal**, not canonical truth and not an executed decision.

## Contract

`ReasoningOutput` contains:

- `context_id` — the DecisionContext being reasoned over;
- `proposal` — machine-readable proposed action/result;
- `rationale` — explicit explanation;
- `evidence_ids` — sorted, unique supporting evidence identifiers;
- `provenance_ids` — sorted, unique provenance identifiers;
- `confidence` — optional numeric confidence in `[0, 1]`.

The object is immutable. No LLM, solver, graph, persistence, or execution dependency is introduced.
