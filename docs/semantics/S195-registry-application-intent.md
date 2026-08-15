# S195 — Registry Application Intent

S195 introduces an explicit immutable application-intent artifact after preflight.

```text
RegistryApplicationPreflight
          ↓
RegistryApplicationIntent
          ↓
[future canonical registry mutation]
```

The intent is not the mutation itself. Creating it does not change the canonical relation registry, graph, ontology, or relation semantics.
