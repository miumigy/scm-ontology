# S257 CI Fix

The S257 regression contract explicitly requires the canonical mutation boundary to state:

- `MUST NOT create a new canonical attribute automatically`
- `MUST NOT mutate canonical facts`

This note records the exact safety invariant required by the S257 regression suite. It does not expand canonical semantics or enable graph mutation.
