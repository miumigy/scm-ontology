# M5 — SCM Use-Case Validation

## Purpose

M5 validates whether the SCM Ontology v0.2 semantic and reasoning foundation can represent and reason about real SCM problems without introducing enterprise-system-specific semantics into the canonical model.

M5 is the transition from **semantic/reasoning foundation** to **SCM applicability validation**.

## Scope

M5 covers representative supply-chain reasoning patterns across:

1. supply dependency
2. site / location dependency
3. material and product flow
4. inventory dependency
5. capacity dependency
6. lead-time dependency
7. supply risk
8. demand / supply alignment
9. enterprise-data mapping

## Validation method

Each use case must be evaluated through the same pipeline:

```text
SCM Business Question
        ↓
Canonical Concept Mapping
        ↓
Canonical Graph Representation
        ↓
RelationPathQuery
        ↓
Explicit Constraints
        ↓
Evidence / Provenance
        ↓
Reasoning Result
        ↓
Explanation / Confidence
```

The validation must demonstrate that the result is reproducible from canonical facts and explicit reasoning rules.

## Canonicality test

A use case passes M5 only when its core semantics can be expressed without requiring:

- SAP-specific concepts
- WMS-specific concepts
- TMS-specific concepts
- planning-product-specific concepts
- vendor-specific identifiers
- certification-framework terminology as canonical ontology concepts

External representations may be mapped through adapters, but adapters must not redefine canonical semantics.

## Evidence requirements

Every non-trivial reasoning result must identify its supporting evidence or explicitly report that evidence is incomplete.

Evidence remains provenance metadata and must not silently become canonical truth.

## Reasoning requirements

A validated use case must preserve the M4 invariants:

- reasoning is read-only by default
- inferred information is not implicitly promoted to canonical truth
- constraints evaluate existing graph paths
- explanations are deterministic
- confidence is derived metadata
- graph mutation is not part of the default reasoning path

## Acceptance criteria

M5 is complete when:

1. At least five representative SCM use cases pass canonicality validation.
2. At least three use cases exercise multi-hop reasoning.
3. Each validated use case has machine-readable input, expected result, evidence, and explanation coverage.
4. At least one ERP/WMS/TMS/planning mapping is demonstrated without changing canonical semantics.
5. Regression tests cover the validated use cases.
6. Any semantic gap discovered during validation is classified as either:
   - missing canonical concept,
   - missing relation semantics,
   - missing reasoning capability,
   - adapter/mapping concern, or
   - intentionally out of scope.
7. No vendor-specific workaround is accepted as a canonical ontology change without explicit architecture review.

## M5 deliverables

- SCM use-case catalog
- canonical mapping examples
- reasoning pattern examples
- enterprise-data mapping examples
- evidence/provenance examples
- regression suite
- semantic-gap report
- M5 validation report

## Exit condition

M5 exits when the project can demonstrate that the v0.2 foundation is not merely internally coherent, but useful for expressing and reasoning about representative SCM problems while remaining enterprise- and framework-independent.

## Non-goals

M5 does not attempt to deliver:

- a production ERP/WMS/TMS integration platform
- an autonomous SCM agent
- a planner or optimizer
- automatic canonical-fact generation
- a complete enterprise ontology
- exhaustive coverage of all SCM processes
