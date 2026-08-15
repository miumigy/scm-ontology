# S273 — M7 Adapter Conformance Contract

## Purpose

Define the minimum conformance contract that every Enterprise Adapter MUST satisfy before it can participate in Canonicalization.

## Conformance boundary

```text
Enterprise Adapter
      ↓
Conformance Checks
      ↓
Canonicalization Contract
      ↓
Eligible Adapter
```

Conformance validates the Adapter Boundary. It does not certify the truth of the enterprise data or authorize new Canonical Semantics.

## Required invariants

A conforming Adapter MUST:

- preserve Enterprise-to-Canonical directionality;
- identify the source representation and adapter version;
- preserve provenance for mapped outputs;
- expose mapping confidence where applicable;
- represent ambiguous mappings explicitly;
- represent unmappable data explicitly;
- preserve Semantic Gap classification;
- preserve the scope of an approved Governance Decision;
- remain traceable to the Mapping Configuration used for execution;
- operate without mutating Canonical Facts as an implicit side effect.

## Forbidden behavior

A conforming Adapter MUST NOT:

- create a new canonical entity, attribute, or predicate automatically;
- mutate canonical facts;
- infer Canonical Truth solely from source labels, vendor codes, mapping success, or adapter behavior;
- silently discard provenance;
- silently resolve ambiguity;
- silently convert unmappable data into a new Canonical concept;
- rewrite historical canonicalization results;
- treat vendor-specific semantics as Canonical Semantics without an explicit approved mapping.

## Conformance result

A conformance check MAY return:

- `conformant`
- `non_conformant`
- `inconclusive`

The result MUST identify the adapter version, mapping configuration version, checked scope, and applicable contract version.

`inconclusive` MUST NOT be interpreted as `conformant`.

## Failure handling

A non-conformant Adapter MUST NOT be presented as eligible for unrestricted Canonicalization. The failure SHOULD identify the violated invariant and relevant evidence.

Conformance failure does not authorize automatic remediation, ontology expansion, or Canonical Fact mutation.

## Regression requirement

Conformance checks SHOULD be repeatable against a fixed Adapter Fixture and MUST be suitable for regression testing when Adapter or Mapping Configuration versions change.

A previously conformant Adapter MUST be re-evaluated when a change can affect its Canonicalization behavior.

## Governance boundary

Conformance is a technical contract check. It is not a Governance Decision and does not approve mappings, ontology changes, or business facts.

Where a conformance failure requires a semantic change, resolution MUST proceed through the applicable Governance process.

## Non-goals

S273 does not define vendor-specific connectors, runtime deployment, automatic remediation, automatic ontology learning, Canonical Fact ingestion, or graph mutation.
