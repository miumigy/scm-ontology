# S270 — M7 Canonicalization Batch Reconciliation Contract

## Purpose

Define a bounded reconciliation mechanism for reviewing multiple Canonicalization outcomes without turning batch comparison into automatic Canonical Truth mutation.

## Reconciliation boundary

```text
Canonicalization Results
        ↓
Batch Reconciliation
        ↓
Difference / Effectiveness Findings
        ↓
Governance Signals
```

Batch reconciliation aggregates observations. It does not establish new business facts.

## Batch identity

A reconciliation MUST preserve:

- `reconciliation_id`
- execution/result references
- adapter version
- mapping configuration version
- reconciliation scope
- reconciliation criteria
- created_at

The reconciliation MUST remain traceable to the individual executions and their provenance.

## Aggregation rules

The reconciliation MAY summarize counts or patterns of:

- identical decisions;
- changed decisions;
- changed canonical targets;
- ambiguous mappings;
- unmappable representations;
- non-reproducible executions;
- effectiveness outcomes.

Aggregated counts MUST NOT erase the underlying result references or their individual provenance.

## Scope boundary

A reconciliation MUST operate only within its declared enterprise, source, mapping, version, and time scope. Results MUST NOT be generalized beyond that scope without a separate controlled assessment.

## Canonical Truth boundary

Batch reconciliation:

- MUST NOT create a new canonical entity, attribute, or predicate automatically;
- MUST NOT mutate canonical facts;
- MUST NOT infer canonical facts from aggregate counts or patterns alone;
- MUST NOT rewrite historical audit records;
- MUST NOT silently change Governance Decisions or approved mappings.

A repeated mapping outcome is evidence about adapter behavior, not proof that the mapped business fact is true.

## Governance handoff

A reconciliation MAY produce Governance Signals when thresholds or review criteria are met. The signal MUST retain references to the underlying observations that caused it.

Threshold crossing MUST NOT itself authorize mapping replacement, ontology expansion, or Canonical Fact mutation.

## Explainability

A reviewer SHOULD be able to move from the reconciliation summary to the affected individual results, versions, provenance, and applicable Governance Decisions.

## Non-goals

S270 does not define automatic remediation, automatic rule optimization, Canonical Fact ingestion, ontology learning, vendor connectors, or graph mutation.
