# S276 — M7 Negative / Canonical Contamination Test Contract

## Purpose

Define negative tests that demonstrate the M7 Adapter boundary rejects enterprise representations that would contaminate Canonical Semantics or Canonical Truth.

## Required rejection cases

A conformant implementation MUST reject or explicitly classify as non-success:

1. an enterprise classification with no approved Canonical mapping;
2. an ambiguous enterprise label where more than one Canonical mapping is plausible;
3. an enterprise field whose provenance is missing or invalid;
4. an enterprise relation whose predicate mapping is not approved;
5. a request to create a new Canonical concept from an unmappable source value;
6. a request to promote a planning or derived artifact into a Canonical Fact without an approved semantic basis;
7. a vendor-specific semantic that has no approved Canonical mapping.

## Canonical contamination invariants

Negative tests MUST demonstrate that the adapter:

- MUST NOT create a new canonical entity, attribute, or predicate automatically;
- MUST NOT mutate canonical facts as a side effect of mapping failure or ambiguity;
- MUST NOT infer Canonical Truth from source labels, vendor codes, or mapping success alone;
- MUST NOT silently resolve ambiguity;
- MUST NOT silently discard provenance;
- MUST NOT convert a Semantic Gap into a new Canonical concept;
- MUST NOT promote Planning / Derived Artifacts into Canonical Facts automatically.

## Expected outcomes

Each negative case MUST produce an observable non-success outcome, explicit Semantic Gap classification, or explicit governance-required outcome. The absence of a Canonical mapping MUST NOT be represented as successful Canonicalization.

## Regression requirement

Negative cases MUST remain part of the regression suite. A future Adapter, Mapping Configuration, or Canonicalization Pipeline change that turns a negative case into silent Canonical creation or mutation MUST fail CI.

## Non-goals

S276 does not define remediation, automatic ontology learning, automatic governance approval, vendor connectors, or production data ingestion.
