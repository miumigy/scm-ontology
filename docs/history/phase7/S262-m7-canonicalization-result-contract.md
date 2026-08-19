# S262 — M7 Canonicalization Result Contract

## Purpose

Define the machine-readable result returned by enterprise canonicalization while preserving the boundary between a mapping result and Canonical Truth.

## Result boundary

```text
Enterprise Representation
        ↓
Mapping
        ↓
Provenance + Semantic Gap
        ↓
Mapping Decision
        ↓
★ Canonicalization Result
```

A Canonicalization Result is the output of an adapter operation. It records what was mapped, what decision was made, and why. It is NOT itself a Canonical Fact.

## Result record

A result SHOULD preserve, where applicable:

- `result_id`
- `source_representation`
- `canonical_target`
- `decision_state`
- `mapping_confidence`
- `provenance`
- `semantic_gap`
- `reason`
- `transformation_metadata`
- `adapter_version`
- `mapping_rule_id`

`canonical_target` MUST be absent or null when no justified canonical target exists.

## Result states

The result MUST preserve the Mapping Decision state defined by S261, including:

`mapped`, `ambiguous`, `unmappable`, `unsupported`, `vendor_specific`, `insufficient_evidence`, `conflicting_semantics`, and `rejected`.

A non-mapped result is a valid result. Failure to produce a canonical target MUST NOT be converted into an arbitrary target, null-suppressed success, or silent discard.

## Result ≠ Canonical Fact

A result with `decision_state = mapped` indicates semantic correspondence, not truth of a business fact.

Therefore:

- a Canonicalization Result MUST NOT be treated as a Canonical Fact automatically;
- `canonical_target` identifies a semantic target, not an asserted business fact;
- `mapping_confidence` is not fact confidence;
- provenance is lineage, not truth;
- transformation metadata explains processing, not business reality.

Any subsequent Canonical Fact assertion requires a separate explicit ingestion/assertion contract outside S262.

## Provenance preservation

The result MUST retain provenance from S259. A transformation MUST retain the original representation reference and relevant transformation metadata. Semantic Gap information from S260 MUST also remain available when applicable.

The result MUST NOT collapse provenance, mapping confidence, and semantic gap into a single opaque status.

## Explainability

Every result MUST expose an explainable `reason` for the decision. Non-success states MUST remain inspectable and MUST NOT be hidden behind exceptions or empty output.

## Read-only invariant

Canonicalization Result creation is read-only with respect to the Canonical Ontology and Canonical Facts. It:

- MUST NOT create a new canonical entity, attribute, or predicate automatically;
- MUST NOT mutate canonical facts;
- MUST NOT infer a canonical fact from the result alone;
- MUST NOT treat `mapped` as equivalent to `true`;
- MUST NOT invent a canonical target to avoid a non-mapped result.

## Determinism

Given equivalent source representation, adapter version, mapping rule version, and relevant context, the result SHOULD be deterministic. Result identifiers MAY be implementation-specific, but the semantic content of the result MUST be explainable and reproducible.

## Downstream contract

Consumers MAY use a Canonicalization Result to:

- populate an adapter audit trail;
- expose provenance and evidence lineage;
- identify semantic gaps;
- request human or governance review;
- prepare a separately governed Canonical Fact assertion.

Consumers MUST NOT interpret the result as permission to mutate the Canonical Ontology or Canonical Graph.

## Non-goals

S262 does not implement canonical fact ingestion, ontology governance, automatic ontology learning, vendor connectors, or graph mutation.
