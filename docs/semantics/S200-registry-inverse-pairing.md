# S200 — Registry Inverse Pairing

S200 makes reciprocal inverse pairing an explicit canonical registry invariant.

For a registered inverse reference:

```text
A → B
B → A
```

An inverse reference that is not yet registered remains permitted for backward compatibility. Once both predicates exist in the canonical registry, their inverse references must point to each other.

Validation is read-only and does not mutate the registry or ontology.
