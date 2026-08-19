# P7-F — Phase 7 Acceptance

## Purpose

P7-F closes **Phase 7 (SCM OS Real Data Plane)** with a deterministic
acceptance contract: heterogeneous inputs are adapted (P7-A), validated
(P7-D), canonicalized (P7-B), identity-resolved (P7-C), and converged into a
reproducible and traceable reference Canonical Graph (P7-E) while preserving the
Canonical Truth boundary.

P7-F composes the P7-A..P7-E reference paths and probes every capability
deterministically. It performs no external side effect and never mutates
Canonical Truth.

## Contract

`src/scm_ontology/phase7_acceptance.py`:

- **`run_phase7_acceptance(*, accepted_at)`** — runs the Phase 7 capability
  probes and returns an immutable, content-addressed `Phase7AcceptanceReport`
  with an overall `accepted` flag.
- **`Phase7AcceptanceReport`** — the serialized record (`contract_version:
  P7F.1`, `is_phase7_acceptance: true`, per-capability `operable` + `evidence_id`,
  and a deterministic `report_id`).

### Capability inventory (P7-A..P7-E)

| key | slice |
|---|---|
| `reference_data_adapter` | P7-A — CSV/JSON/SQL adapters → `SourceEvidence` |
| `mapping_canonicalization` | P7-B — `CanonicalizationResult` |
| `identity_resolution` | P7-C — identity matches / conflicts |
| `data_quality_freshness_gate` | P7-D — completeness/freshness/scope/unit/provenance |
| `multi_source_reference_convergence` | P7-E — converged reference Canonical Graph |

### Phase 7 acceptance criterion

The phase is **accepted** when every capability is operable AND the converged
reference graph (P7-E) is simultaneously:

- **reproducible** — identical content hash and JSON across runs;
- **traceable** — every node carries source members, every edge carries
  provenance, and identity links reference resolved members;
- **reference-boundary** — `canonical_truth_boundary = "reference"` (never
  Canonical Truth).

## Fail-closed behavior

- `accepted_at` must be non-empty.
- Any capability probe that raises or returns no usable output is recorded as
  `operable: false` and blocks acceptance (never silently treated as passed).

## Determinism & provenance

- The same `accepted_at` produces an identical report (`report_id` and JSON).
- Each capability retains an `evidence_id` (content hash of its deterministic
  output) for audit / replay.

## Non-goals

P7-F does not:

- mutate Canonical Truth, the Canonical Ontology, or the Canonical Graph;
- perform the separate governed application boundary to Canonical Truth;
- add vendor connectors, schedulers, or third-party dependencies.
