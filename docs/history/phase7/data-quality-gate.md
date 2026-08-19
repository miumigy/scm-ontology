# P7-D — Data Quality / Freshness Gate

## Purpose

P7-D is the fourth **Phase 7 (SCM OS Real Data Plane)** slice. It provides a
deterministic, **read-only quality / freshness gate** that validates the
**completeness, freshness, scope, unit, and provenance** of P7-A `SourceEvidence`
before it proceeds to canonicalization.

```text
SourceEvidence (P7-A)
        ↓
 DataQualityPolicy  (explicit scope / freshness / unit / required-fields)
        ↓
 DataQualityGate.evaluate
        ↓
 per-record per-check  pass / warn / fail
        ↓
 DataQualityReport   (blocked = any record failed)   → fail closed
```

The gate is fail-closed: a batch that fails any required check is flagged
`blocked` and never silently proceeds. It performs no mapping (P7-B), no
identity resolution (P7-C), and no canonicalization or mutation.

## Contract

`src/scm_ontology/data_quality_gate.py` defines:

- **`DataQualityPolicy`** — explicit governance bounds: required fields,
  allowed scopes, unit constraints, maximum evidence age, and whether
  provenance is mandatory.
- **`UnitConstraint`** — an allowed unit set for a declared evidence field
  (representation only; never semantic invention).
- **`DataQualityGate`** — evaluates every record in a `SourceDataset`
  (or `evaluate_many` across several) and returns an immutable
  `DataQualityReport`.
- **`QualityCheckResult` / `RecordQuality`** — explicit per-check and per-record
  `pass` / `warn` / `fail` outcomes.
- **`DataQualityReport`** — deterministic aggregate (`evaluated_count`,
  `passed_count`, `failed_count`, `blocked`, content-sorted JSON).

### Checks (S309 / P7-D roadmap contract)

| Check | Meaning |
|---|---|
| `completeness` | every `required_fields` entry is present |
| `freshness` | `observed_at` is within `max_age_seconds` of the gate `now` (or no policy) |
| `scope` | `record.scope` is in `allowed_scopes` |
| `unit` | declared unit fields use an allowed unit (missing optional fields pass) |
| `provenance` | `source_location` and field-level `field_evidence` are present |

## Fail-closed behavior

The gate MUST:

- reject a blank / non-unique policy or empty `allowed_units`;
- flag `blocked = True` when any record fails any required check;
- report `pass` / `warn` / `fail` explicitly (never rely on absence of errors);
- remain deterministic: identical input + `now` produces an identical report.

## Canonical safety

A quality report is metadata about evidence, never Canonical Truth. The gate
does not map, resolve identity, or mutate anything. It composes the P7-A
`SourceEvidence` / `SourceDataset` boundary without weakening it.

## Deterministic reference path

`run_reference_data_quality_path()` evaluates the P7-A ERP material-master
evidence against a reference policy (required `material_id` + `description`,
`enterprise:acme` scope, 24h freshness) and reports `passed`/`blocked=False`,
deterministically.

## Non-goals

P7-D does not:

- canonicalize or map source data (P7-B), resolve identity (P7-C);
- mutate Canonical Truth, the Canonical Graph, or the Canonical Ontology;
- run live systems, freshness monitoring, or a scheduler;
- add vendor connectors or third-party dependencies (stdlib only).
