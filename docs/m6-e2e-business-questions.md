# S253 — M6 End-to-End Business Questions

## Purpose

Validate that executable M6 graph fixtures can answer SCM business questions through a deterministic read-only reasoning path.

## E2E contract

```text
Business Question
      ↓
Canonical Query
      ↓
Graph Path Resolution
      ↓
Evidence / Provenance
      ↓
Explanation
      ↓
Confidence
      ↓
Business Answer
```

## Representative questions

### Q-001 — Supply dependency

Which supplier and physical site support a focal material?

Expected canonical path:

`Material → supplied_by → Supplier → located_at → Site`

### Q-003 — Inventory location

Where is a focal material stocked?

Expected canonical path:

`Material → stocked_at → Inventory Position → located_at → Site`

### Q-004 — Capacity provider

Which site provides the capacity required by an activity?

Expected canonical path:

`Activity → requires_capacity → Capacity Resource → provided_by → Site`

### Q-005 — Supply risk

Which explicitly represented supply risk is associated with the site supporting a focal material?

Expected canonical path:

`Material → supplied_by → Supplier → located_at → Site → exposed_to → Supply Risk`

## M6 acceptance contract

Each question must produce:

- a deterministic canonical path
- referenced evidence
- an explanation based only on resolved graph facts
- confidence derived from explicit evidence/factors
- no graph mutation
- no implicit canonical-fact creation
- explicit `no_match` for unresolved paths

## Boundary

The E2E layer validates integration between Graph, Query, Reasoning, Evidence, Explanation, and Confidence. It does not introduce new canonical concepts merely to make a fixture answerable.
