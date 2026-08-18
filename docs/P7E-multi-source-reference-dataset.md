# P7-E — Multi-source Reference Dataset

## Purpose

P7-E is the fifth **Phase 7 (SCM OS Real Data Plane)** slice. It composes the
P7-A Reference Data Adapter, P7-B Mapping / Canonicalization Runtime, P7-C
Identity Resolution Runtime, and P7-D Data Quality / Freshness Gate into one
**reproducible, traceable** pipeline in which several heterogeneous source
representations converge onto a single **reference Canonical Graph**.

```text
ERP @csv ─┐
WMS @json ┼─ P7-A adapters -> SourceEvidence
TMS @sql ─┘        │
                   ├─ P7-D quality gate (fail closed)
                   ├─ P7-B canonicalization -> CanonicalizationResult
                   ├─ P7-C identity resolution -> matched identities
                   ▼
          ConvergedReferenceGraph (reproducible + traceable)
```

## Contract

`src/scm_ontology/multi_source_reference.py`:

- **`converge(...)`** — fails the pipeline closed through the P7-D gate, then
  runs P7-B canonicalization and P7-C identity resolution over the mapped
  records of the requested identity types, and builds the converged view.
- **`ConvergedReferenceGraph`** — an immutable, content-addressed
  (`content_hash`) reference graph with `nodes`, `edges`, `identity_links`, and
  an explicit **`canonical_truth_boundary = "reference"`**.
- **`ConvergedNode`** — one canonical entity node with its source members
  (source system, record, provenance).
- **`ConvergedEdge`** — a canonical predicate edge whose endpoints resolve to
  converged nodes (e.g. `Shipment -carriedBy-> Product`).

## Convergence & traceability

- ERP (product master) and a second WMS product registry reference the same
  canonical Products via a shared explicit GTIN identity signal.
- Identity resolution (P7-C) matches them, and each `Product` node converges
  from **two source systems** onto one canonical reference.
- A TMS shipment keeps a distinct `Shipment` node and contributes a `carriedBy`
  predicate edge that resolves to the converged Product node.
- Every node / edge / identity link is traceable to its source evidence.

## Canonical safety

The converged graph is a **reference projection**, never Canonical Truth
(`canonical_truth_boundary = "reference"`). It is deterministic (identical JSON
and content hash across runs), fail-closed (the quality gate blocks any flat
batch), and read-only: the pipeline maps, validates, resolves identity, and
projects, but never mutates Canonical Truth, the Canonical Ontology, or the
Canonical Graph.

## Fail-closed behavior

`converge` MUST:

- reject an empty dataset list;
- raise `MultiSourceError` if any source lacks a quality policy or fails it;
- refuse to converge a batch whose quality gate is `blocked`.

## Deterministic reference path

`run_multi_source_reference_path()` produces 4 nodes:
- `Product` nodes `0850000000101` / `0850000000102`, each fused from ERP + WMS;
- `Shipment` nodes `SHIP-1` / `SHIP-2` from TMS;

plus 2 `carriedBy` edges and 2 identity links — reproducibly.

## Non-goals

P7-E does not:

- mutate Canonical Truth, the Canonical Ontology, or the Canonical Graph;
- create canonical entities / attributes / predicates automatically;
- run live systems, schedulers, or a database;
- act as the governed application boundary (that remains an explicit,
  separately-governed step);
- add vendor connectors or third-party dependencies (stdlib only).
