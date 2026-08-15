# S220 — Reasoning Contract Hardening

S220 fixes the lifecycle/status contract for reasoning results.

Allowed statuses are:

- `matched`: at least one canonical match is required.
- `no_match`: the result must contain no matches.
- `failed`: the result must contain no matches.

Unsupported statuses are rejected.

```text
Query → Evaluation → Evidence → Result → Contract Validation
```

This boundary validates the result contract only. It does not execute inference, mutate the graph, or reinterpret evidence.
