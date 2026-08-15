# S231 — Advanced Path Constraints

S231 extends explicit path constraints without introducing inference.

Supported constraints:

- `PathEndsAt(node_id)` — terminal node equality
- `PathContainsNode(node_id)` — node membership
- `PathContainsPredicate(predicate_ref)` — predicate occurrence

All constraints evaluate only paths already returned by canonical traversal.

```text
Canonical Graph
    ↓
Existing Path
    ↓
Explicit Constraint
    ↓
Filtered Path
```

No constraint creates, repairs, or infers a path.
