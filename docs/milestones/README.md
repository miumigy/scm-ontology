# SCM Ontology Milestones

## Status overview

| Milestone | Focus | Status |
|---|---|---|
| M1 | Canonical Semantic Foundation | ✅ Complete |
| M2 | Canonical Graph / Query Foundation | ✅ Complete |
| M3 | Evidence / Provenance Foundation | ✅ Complete |
| M4 | Reasoning Runtime Foundation | ✅ Complete |
| v0.2 RC | Semantic / Reasoning Foundation Release Candidate | ✅ Complete |
| M5 | SCM Use-Case Validation | ✅ Complete |
| M6 | SCM Graph Integration | ✅ Complete |
| M7 | Enterprise Canonicalization | ✅ Complete |
| **M8** | **Canonicalization, Projection & Operational Governance** | **✅ Complete** |

## M8 closeout

M8 is the current completed milestone. It establishes the governed lifecycle from enterprise evidence to Canonical Truth and through historical query, projection, materialization, invalidation, cross-projection consistency, and operational governance.

See [`M8-acceptance-report.md`](./M8-acceptance-report.md) for the acceptance summary and [`S310-m8-acceptance-closure.md`](./S310-m8-acceptance-closure.md) for the normative closure contract.

## M8 slice map

```mermaid
flowchart LR
    S294[Conflict / Resolution] --> S300[Fact Lifecycle]
    S300 --> S301[Fact Application]
    S301 --> S302[Historical Query]
    S302 --> S303[Graph Read / Projection]
    S303 --> S304[Freshness / Lineage]
    S304 --> S305[Projection Query]
    S305 --> S306[Materialization]
    S306 --> S307[Invalidation]
    S307 --> S308[Consistency / Rebuild]
    S308 --> S309[Operational Governance]
    S309 --> S310[M8 Acceptance]
```

## Historical milestone documents

Completed milestone documents are intentionally retained as historical records. When an older document says a later phase is "next" or "active", interpret that statement in the context of the document's historical point in time; the status table above is the current source of truth.

## Next phase

There is intentionally no automatic M9 expansion in this document. Post-M8 work should be selected from the implementation roadmap after reviewing the contract-complete architecture and identifying the highest-value reference implementation.
