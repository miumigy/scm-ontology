# S21 — Domain Extension Contract

S21 defines how SCM-specific concepts extend the Core semantic primitives established in S10–S20.

## Contract

Every domain extension must explicitly declare:

```text
DomainExtension
├─ name
├─ core_primitive
└─ definition
```

A domain concept is an extension, not a replacement for Core semantics.

## Example

```text
Inventory
   │
   └─ core_primitive → Entity
```

The domain layer may add SCM-specific attributes, relationships, constraints, and vocabularies, while preserving the meaning of the referenced Core primitive.

## Non-goals

S21 does not:

- redefine Core primitives
- require every domain concept to become a Core primitive
- prescribe a universal SCM vocabulary
- introduce automatic inference between domain concepts
- mix source-system mappings into Core

## Design rule

A proposed SCM concept should first answer:

1. Which Core primitive does it extend?
2. What domain-specific meaning does it add?
3. Which constraints are domain-specific?
4. Which relationships are domain-specific?
5. Why does the concept not belong in Core?

If these questions cannot be answered explicitly, the concept should not yet be promoted into the domain ontology.
