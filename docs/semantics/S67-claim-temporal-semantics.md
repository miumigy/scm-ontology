# S67 — Claim Temporal Semantics

## Purpose

S67 defines the minimal canonical interval that describes when a Claim is semantically applicable.

```text
Claim
  └─ validity
       ├─ valid_from
       └─ valid_to
```

Both bounds are optional. `null` means the corresponding boundary is open.

## Semantic boundary

Claim validity answers:

> When does this claim apply or hold?

It does **not** answer:

- when the claim was observed;
- when the claim was asserted;
- when an evidence source was created;
- when an event occurred;
- when provenance was recorded.

Those are separate temporal semantics and are intentionally outside S67.

## Representation

S67 uses lightweight temporal references rather than imposing a timestamp implementation, timezone policy, interval arithmetic, or database temporal-table semantics.

The values are therefore represented as optional strings at this layer. Interpretation of the temporal reference is deferred to a later canonical time contract.

## Boundary with Relationship Validity

Relationship validity and Claim validity are distinct semantic objects even though both may use `valid_from` / `valid_to`.

```text
Relationship validity
    = when a relationship is valid

Claim validity
    = when a claim is applicable / holds
```

The shared field names do not imply that the two contracts are interchangeable.

## Deliberately deferred

S67 does not define:

- observation time
- assertion time
- event time
- transaction time
- timezone policy
- inclusive/exclusive boundary rules
- interval arithmetic
- temporal reasoning
- contradiction resolution
