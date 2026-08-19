# S268 — M7 Governance Decision Application Contract

## Purpose

Define the controlled application boundary for an approved Governance Decision without allowing governance review to become implicit Canonical Truth mutation.

## Application boundary

```text
Governance Decision
      ↓
Decision Scope / Version Check
      ↓
Controlled Application
      ↓
Updated Mapping Configuration
      ↓
Future Canonicalization Runs
```

An approved decision affects only the explicitly approved scope and version. It MUST NOT retroactively rewrite historical canonicalization results.

## Preconditions

Before application, the system MUST verify:

- the decision state is `approved`;
- the decision is traceable to its Governance Signal;
- the mapping rule and adapter versions are identified;
- the approved scope is explicit;
- required evidence and provenance references remain available.

If a precondition fails, application MUST NOT proceed silently.

## Forward-only effect

A successfully applied decision changes the configuration used by subsequent canonicalization executions. It MUST NOT silently modify historical audit records, historical replay results, or prior canonicalization decisions.

Historical executions remain associated with the mapping and adapter versions that produced them.

## Versioning

Application MUST produce an identifiable mapping configuration version or equivalent controlled version reference. A future canonicalization run MUST be able to identify which approved decision and configuration version it used.

## Canonical Truth boundary

Applying an approved mapping decision:

- MUST NOT create a new canonical entity, attribute, or predicate automatically unless that exact action was separately approved under ontology governance;
- MUST NOT mutate existing canonical facts as a side effect;
- MUST NOT infer a canonical fact from the approval or configuration change alone;
- MUST NOT rewrite historical audit records;
- MUST NOT retroactively reclassify prior canonicalization results without a separate controlled process.

## Scope isolation

An approved decision for one enterprise representation, field, relation, source system, or defined scope MUST NOT implicitly apply to unrelated representations.

Vendor-specific semantics remain behind the Adapter Boundary unless separately mapped and approved.

## Failure handling

If application fails, the previous effective configuration MUST remain identifiable and historical records MUST remain intact. A partial application MUST be observable and MUST NOT be represented as a successful governance decision application.

## Explainability

A future canonicalization execution using an applied decision SHOULD be able to identify:

- the Governance Decision;
- the effective configuration version;
- the mapping rule version;
- the adapter version;
- the approved scope.

## Non-goals

S268 does not define a deployment platform, runtime implementation, automatic approval, retroactive migration of canonical facts, automatic ontology learning, vendor connectors, or graph mutation.
