# S265 — M7 Replay Difference / Change Classification Contract

## Purpose

Define how a replay is compared with its historical Canonicalization Result without silently rewriting history or treating differences as Canonical Truth.

## Difference boundary

```text
Historical Result
      ↓
Replay Result
      ↓
★ Difference Classification
      ↓
Review / Governance Signal
```

A Difference Classification describes a change in adapter behavior. It is not a business fact.

## Required classifications

A comparison MUST distinguish at least:

- `same_decision`
- `changed_decision`
- `changed_canonical_target`
- `changed_mapping_confidence`
- `changed_provenance`
- `changed_semantic_gap`
- `non_reproducible`

The classification MUST preserve enough context to explain which dimensions changed.

## Version-aware comparison

Historical and replay results MUST be compared together with their `mapping_rule_version` and `adapter_version`. A difference caused by a version change MUST remain attributable to that version change.

## No silent normalization

A changed or non-reproducible replay MUST NOT be silently normalized to the historical result. The difference MUST remain explicit and reviewable.

## Governance signal

A difference MAY trigger adapter review, mapping-rule review, evidence review, or governance workflow. A difference MUST NOT by itself authorize Canonical Ontology or Canonical Fact mutation.

## Canonical Truth boundary

Difference Classification is read-only with respect to Canonical Truth. It:

- MUST NOT create a new canonical entity, attribute, or predicate automatically;
- MUST NOT mutate canonical facts;
- MUST NOT infer a canonical fact from a difference classification alone;
- MUST NOT rewrite historical audit records;
- MUST NOT interpret `same_decision` as proof that the underlying business fact is true.

## Explainability

A difference SHOULD expose the historical value, replay value, and relevant version/context for every changed dimension. `non_reproducible` MUST include an explainable reason when the replay environment cannot reproduce the historical execution.

## Non-goals

S265 does not implement automatic remediation, canonical fact ingestion, ontology governance, automatic ontology learning, vendor connectors, or graph mutation.
