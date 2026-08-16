# S311 — Governed Canonical Graph Persistence Planning

S311 introduces the first implementation boundary between the transport-neutral `CanonicalGraph` and a future graph-store adapter.

## Contract

```text
CanonicalGraph
    -> PersistenceAuthorization
    -> CanonicalGraphPersistencePlanner
    -> PersistencePlan
    -> future GraphStoreAdapter
```

The planner creates a deterministic persistence **intent**. It does not write to Neo4j, mutate Canonical Truth, create identities, or resolve references.

## Required governance inputs

- `decision_id`: explicit authorization decision reference
- `actor`: accountable actor
- `scope`: governed persistence scope
- `authorized`: explicit allow/reject decision
- `reason`: optional decision rationale

## Determinism

The plan contains a SHA-256 digest of the canonical graph serialization. The plan ID is derived deterministically from the graph digest and authorization envelope.

Therefore identical graph + authorization inputs produce the same plan identity, while changing the graph or authorization envelope changes the plan identity.

## Safety boundary

An unauthorized request produces `rejected`; it is never converted into a write attempt. An authorized request produces `planned`, not `applied`.

`planned` is intentionally not evidence that a graph store accepted or persisted the data. The future adapter must remain a separate execution boundary.
