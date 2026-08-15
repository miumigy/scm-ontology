# S199 — Registry Integrity

S199 validates the canonical relation registry after functional mutation.

Invariants:

- predicate references are unique;
- an inverse reference may point to an as-yet-unregistered predicate;
- when an inverse reference is itself registered as a predicate, the two declarations must be reciprocal.

```text
Canonical Registry
       ↓
Integrity Validation
       ├─ predicate uniqueness
       └─ registered inverse reciprocity
```

This preserves the existing canonical relation model, where inverse references can be declared before their inverse predicate is registered. Validation is read-only and does not mutate the registry or ontology.
