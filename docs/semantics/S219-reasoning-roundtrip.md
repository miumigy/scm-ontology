# S219 — Graph ↔ Reasoning Round-trip

S219 fixes the scope invariant between a reasoning query and its result.

```text
CanonicalGraph
   ↓
NodeQuery
   ↓
ReasoningResult
```

Every result match must resolve within the node set selected by the originating query. A result cannot silently introduce an out-of-scope canonical identity.

The validator is read-only and does not modify graph or reasoning state.
