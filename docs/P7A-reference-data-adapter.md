# P7-A — Reference Data Adapter

## Purpose

P7-A is the first **Phase 7 (SCM OS Real Data Plane)** slice. It moves the SCM
OS from reference/in-memory fixtures toward heterogeneous enterprise data while
**preserving the Canonical Truth boundary**.

P7-A provides portable **CSV / JSON / SQL source adapters** that turn arbitrary
enterprise representations into an explicit, provenance-bearing **source
evidence** set. It is strictly the *adapter* side of the data plane:

```text
CSV / JSON / SQL  -->  Source Adapter  -->  Source Evidence (this slice)
                                                    |
                 (P7-B Canonicalization) <----------+
                 (P7-C Identity Resolution)
                 (P7-D Data Quality / Freshness Gate)
                 (P7-E Multi-source Reference Dataset)
```

Per the roadmap design rule, P7-A starts with **portable reference adapters**,
not a vendor-specific connector program. SAP / WMS / TMS / MES connectors become
implementations of the same boundary later.

## Contract

`src/scm_ontology/reference_data_adapter.py` defines three adapter kinds
(`adapt_csv`, `adapt_json`, `adapt_sql`) and a deterministic reference path
(`run_reference_data_adapter_path`). Every adapter:

- takes a **`SourceManifest`** (source system, adapter version, data-contract
  version, mapping-config version, extraction timestamp, and explicit scope);
- returns an immutable **`SourceDataset`** of **`SourceEvidence`** records;
- attaches **field-level provenance** (`EvidenceRef`) to every payload field;
- is **fail-closed** on missing source identity, identity column / primary key,
  scope, provenance, or extraction timestamp.

### Evidence, not truth

P7-A completes the boundary from **Enterprise Representation → Source
Evidence**. It does **not** perform source-to-canonical mapping, identity
resolution, or Canonical Fact creation. That is what keeps later slices
(P7-B canonicalization, P7-C identity resolution) separated and correct.

Evidence is a **reference** (`SourceEvidence.as_evidence_reference()` yields an
`EvidenceReference` of type `source_reference`). A successful adapter run must
never be read as Canonical Truth.

## Adapters

| Adapter | Input | Identity | Source location |
|---|---|---|---|
| CSV | decoded rows (dicts) | `record_id_column` | `{path}:row={row_number}` |
| JSON | object `{records:[...]}` or array | `record_id_key` | `{path}[{index}]` |
| SQL | injected row provider (backend-neutral) | `primary_key` | `sql:{table}:{primary_key}` |

The SQL adapter is **backend-neutral**: it never imports a database driver and
accepts an iterable of rows (e.g. a sqlite3 cursor, a test stub, or any backend
adapter). This keeps the deterministic reference path free of external
infrastructure, per the cross-phase principle "deterministic reference path
first".

## Multi-source boundary

`run_reference_data_adapter_path()` converges one ERP (`@csv`), one WMS
(`@json`), and one TMS (`@sql`) source into a single
**`ReferenceEvidenceBundle`**. Each source keeps its own manifest, scope, and
source-system identity. A shared `record_id` value across sources stays **distinct
evidence** — the bundle never collapses or resolves identity.

## S273 conformance

`conformant(dataset)` returns an `AdapterConformance` result with the S273
vocabulary (`conformant` / `non_conformant` / `inconclusive`) plus the adapter
version, mapping-config version, contract version, and checked scope.
`inconclusive` is never treated as `conformant`. Because the manifest is
fail-closed, a validly constructed dataset always reports `conformant`; the
other outcomes preserve the S273 contract for future connector implementations
and are never silently promoted.

## Fail-closed behavior

The adapters MUST reject:

- a `SourceManifest` with any blank field or an unsupported `adapter_kind`;
- a dataset with zero records, or records whose scope / source system /
  mapping-config version differ from the manifest;
- a CSV row without the configured identity column, or with an empty or
  duplicate record id;
- a JSON payload without a `records` list, or a record missing / duplicating its
  identity key;
- a SQL row without the configured primary key, or with an empty / duplicate
  primary-key value, or a scope mismatch.

## Determinism & provenance

- Identical input produces an identical `SourceDataset` (content-addressed
  `content_hash`) and identical bundle JSON.
- Every evidence record is immutable (`frozen` dataclass) and carries
  `evidence_id`, `source_location`, `record_id`, field-level `EvidenceRef`
  provenance, `observed_at`, `scope`, and `mapping_config_version`.

## Non-goals

P7-A does not:

- map source fields to canonical concepts (that is P7-B);
- resolve identity across source systems (that is P7-C);
- run data-quality or freshness gates (that is P7-D);
- mutate Canonical Truth or any external store (evidence only, read-only);
- introduce a new canonical Entity, Relationship, or derived-state type;
- add a vendor connector, a database driver, or a web dependency (stdlib only,
  backend-neutral SQL).
