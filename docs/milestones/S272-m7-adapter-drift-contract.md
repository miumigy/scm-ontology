# S272 — M7 Adapter Drift Detection Contract

## Purpose

Define how changes in enterprise representations, adapter behavior, or mapping configuration are detected and classified without silently changing Canonical Semantics.

## Drift boundary

```text
Enterprise Representation / Adapter / Mapping
                    ↓
              Drift Detection
                    ↓
             Drift Classification
                    ↓
             Governance Signal
```

Drift detection identifies a change. It does not decide that the changed representation is a new Canonical concept or business fact.

## Drift dimensions

A drift assessment MAY identify changes in:

- enterprise field structure or datatype;
- source-system relation or identifier behavior;
- adapter transformation behavior;
- mapping-rule version;
- mapping target;
- mapping confidence;
- provenance availability;
- semantic-gap classification;
- approved decision scope.

Each detected drift MUST identify the affected version or observation where possible.

## Classification

A drift MAY be classified as:

- `representation_drift`
- `adapter_behavior_drift`
- `mapping_drift`
- `provenance_drift`
- `semantic_gap_drift`
- `scope_drift`
- `inconclusive_drift`

The classification is a review signal, not a Canonical Truth assertion.

## Version and history boundary

Drift detection MUST preserve the versions being compared and MUST NOT rewrite historical adapter decisions, canonicalization results, or audit records.

A current representation MUST NOT be treated as if it had always used the current mapping.

## Canonical Truth boundary

Drift detection:

- MUST NOT create a new canonical entity, attribute, or predicate automatically;
- MUST NOT mutate canonical facts;
- MUST NOT infer a canonical fact from drift alone;
- MUST NOT silently replace an approved mapping;
- MUST NOT expand the Canonical Ontology merely because a representation changed.

## Governance handoff

Material drift MAY produce a Governance Signal. Resolution MUST follow the applicable controlled Governance Decision process.

Detection of drift MUST NOT itself authorize mapping replacement, ontology extension, or Canonical Fact mutation.

## Explainability

A drift finding SHOULD identify the compared versions, affected scope, changed dimensions, evidence references, and classification rationale.

## Non-goals

S272 does not define automated remediation, automatic rule replacement, ontology learning, Canonical Fact ingestion, vendor connectors, or graph mutation.
