# S171 — Relation Validation Result

S171 separates validation outcome from semantic truth.

## Statuses

- `pass`: the relation satisfies the current canonical contract.
- `review`: the relation is known, but its domain/range typing requires review.
- `extension`: the predicate is outside the canonical vocabulary and may belong to an extension/mapping layer.
- `error`: reserved for malformed validation input or future hard validation failures.

A validation result is metadata about model conformance. It is **not** an assertion about the business world.

In particular:

```text
validation failure ≠ false fact
validation pass    ≠ business truth
extension          ≠ canonical concept
```

This distinction allows enterprise mappings to preserve source semantics while keeping the canonical core controlled.
