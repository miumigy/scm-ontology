# S165 — Canonical Relation Model

S165 establishes a controlled registry for canonical relation predicates.

## Semantic classes

Relations are classified as:

- physical
- informational
- temporal
- causal
- epistemic
- organizational
- operational
- governance

The registry intentionally starts with a small set of reusable predicates rather than enumerating every business relationship.

## Examples

```text
located_at
contains
part_of
transforms
consumes
produces
supplies
fulfills
allocated_to
reserved_for
committed_to
planned_for
scheduled_for
executes
flows_through
measured_by
evaluated_by
decided_by
results_in
```

## Important boundaries

- A relation predicate is not an assertion; an assertion supplies subject, object, and context.
- An inverse predicate is a semantic navigation aid, not a second fact unless explicitly asserted or derived by policy.
- Relation kind does not determine causality. Only predicates explicitly classified as causal carry causal semantics.
- Business-specific relationship names belong in mapping layers, not the canonical registry.
