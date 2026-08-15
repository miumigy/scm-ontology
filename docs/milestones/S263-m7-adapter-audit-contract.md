# S263 — M7 Adapter Auditability Contract

## Purpose

Define an auditable record of enterprise canonicalization decisions so that a reviewer can reconstruct why a Canonicalization Result was produced without treating the audit record as Canonical Truth.

## Audit boundary

```text
Enterprise Representation
        ↓
Mapping / Transformation
        ↓
Mapping Decision
        ↓
Canonicalization Result
        ↓
★ Adapter Audit Record
```

An Adapter Audit Record describes processing history and decision lineage. It is metadata about canonicalization, not a business fact.

## Required audit lineage

An audit record MUST preserve, where applicable:

- `audit_id`
- `result_id`
- `source_system`
- `source_representation`
- `mapping_rule_id`
- `adapter_version`
- `decision_state`
- `mapping_target`
- `mapping_confidence`
- `provenance`
- `semantic_gap`
- `reason`
- `transformation_metadata`
- `recorded_at`

The lineage MUST be sufficient to identify the source representation, the mapping rule and adapter version used, the resulting decision, and the explanation for that decision.

## Immutability

Once an audit record has been recorded, the audit history MUST be append-only. Corrections MUST be represented by a new audit record or explicit superseding event rather than silently rewriting the historical decision. The audit process MUST NOT silently rewrite the historical decision.

Audit immutability does not imply that the source business data is true or immutable.

## Reproducibility

A reviewer SHOULD be able to reconstruct the semantic decision from the recorded source representation reference, mapping rule, adapter version, relevant provenance, semantic-gap classification, and reason.

A later adapter version MUST NOT rewrite historical audit records. A changed mapping rule creates a new decision lineage.

## Explainability

Every audit record MUST expose the decision state and an explainable `reason`. Non-mapped outcomes MUST remain auditable, including `ambiguous`, `unmappable`, `unsupported`, `vendor_specific`, `insufficient_evidence`, `conflicting_semantics`, and `rejected`.

## Temporal context

`recorded_at` identifies when the adapter recorded the decision. It MUST NOT be confused with the effective time of the underlying enterprise business data. Where source temporal context is available, it SHOULD be retained separately in provenance or transformation metadata.

## Canonical Truth boundary

An audit record MUST NOT be interpreted as a Canonical Fact merely because it records a `mapped` result.

In particular:

- provenance is lineage, not truth;
- mapping confidence is confidence in semantic correspondence, not fact confidence;
- an audit record is evidence about adapter processing, not evidence that the underlying business event occurred;
- audit history MUST NOT be used as an implicit canonical-fact ingestion mechanism.

## Read-only invariant

Audit recording is read-only with respect to the Canonical Ontology and Canonical Facts. The adapter:

- MUST NOT create a new canonical entity, attribute, or predicate automatically;
- MUST NOT mutate canonical facts;
- MUST NOT infer a canonical fact from an audit record alone;
- MUST NOT rewrite historical audit decisions to conceal mapping errors or semantic gaps.

## Governance boundary

Audit records MAY be used for adapter quality analysis, mapping-rule review, evidence collection, human review, or ontology-governance proposals. Those activities are separate workflows and MUST NOT mutate the Canonical Ontology as a side effect of audit recording.

## Non-goals

S263 does not define a database implementation, audit retention policy, canonical fact ingestion, ontology governance procedures, automatic ontology learning, vendor connectors, or graph mutation.
