# S237 — SCM Use-Case Validation Catalog

## Purpose

Establish the first machine-oriented catalog of representative SCM business questions for M5 validation.

## Catalog

| ID | Use case | Canonical reasoning path | Validation intent |
|---|---|---|---|
| UC-01 | Supply dependency | `depends_on → supplied_by` | identify upstream supply dependency |
| UC-02 | Site dependency | `supplied_by → located_at` | trace dependency to physical site |
| UC-03 | Material flow | `moves → from → to` | trace physical movement |
| UC-04 | Inventory dependency | `stocked_at → serves` | connect inventory position to demand/service context |
| UC-05 | Capacity dependency | `requires_capacity → provided_by` | trace resource dependency |
| UC-06 | Lead-time dependency | `has_lead_time → affects` | identify timing dependency |
| UC-07 | Supply risk | `depends_on → supplied_by → located_at` | expose multi-hop supply exposure |
| UC-08 | Demand/supply alignment | `demanded_by → supplied_by` | compare demand-side and supply-side relationships |
| UC-09 | Enterprise mapping | adapter-specific representation → canonical relation | validate semantic independence |

## Validation contract

Every catalog item must eventually specify:

- business question
- canonical concepts
- canonical predicates
- path query
- explicit constraints
- expected result
- evidence requirements
- explanation requirements
- confidence factors
- semantic-gap classification

The catalog is intentionally not an ontology extension. A missing predicate or concept discovered during validation must first be classified as a semantic gap before any canonical-model change is proposed.

## S237 acceptance

S237 is complete when the catalog is committed and each use case has a stable identifier that can be referenced by subsequent validation tests and reports.
