# P7-C — Identity Resolution Runtime

## Purpose

P7-C is the third **Phase 7 (SCM OS Real Data Plane)** slice. It provides
deterministic, **governed entity matching** that decides whether distinct source
identities refer to the same Canonical Entity, with first-class **ambiguous /
unresolved / conflict** outcomes — never coerced into a match.

P7-C composes the P7-A Reference Data Adapter (`SourceEvidence`) and the P7-B
Mapping / Canonicalization Runtime (`CanonicalizationResult`). Identity signals
are *explicitly declared* canonical attributes from the governing policy; the
resolver never infers identity from field-name resemblance, similarity scores,
or adapter / mapping success.

```text
CanonicalizationResult (P7-B)
        ↓
 IdentityRecord.from_canonicalization
        ↓
 IdentityResolutionPolicy (explicit signals)
        ↓
 IdentityResolver.identify
        ↓
 IdentityCandidate  →  IdentityDecision (append-only)
        ↓
 canonical_mutation = false   (a decision, never a Canonical Fact)
```

## Contract

`src/scm_ontology/identity_resolution_runtime.py` defines:

- **`IdentitySignal`** — an explicitly declared canonical attribute used as an
  identity-key signal.
- **`IdentityResolutionPolicy`** — the governing policy (id + version + signals)
  used to reach a decision.
- **`IdentityRecord`** — wraps a mapped P7-B `CanonicalizationResult`; unmapped
  results are rejected.
- **`IdentityCandidate`** — a proposed (not yet governed) correspondence with an
  S297 outcome (`matched` / `not_matched` / `ambiguous` / `unresolved` /
  `conflict`) plus attributed evidence.
- **`IdentityDecision`** — an append-only S290 decision
  (`accepted_for_governed_application` / `rejected` / `unresolved` /
  `conflicting` / `deferred_for_review`) linked to prior decisions.
- **`IdentityResolutionRun`** — a deterministic, replayable aggregate.

### Resolution outcomes (S297)

| Outcome | When |
|---|---|
| `matched` | one record per source, sharing a key, aligned on one canonical entity |
| `not_matched` | a key present in only one source system |
| `ambiguous` | multiple records share a key on one source; no unique member set |
| `unresolved` | identity signal missing / blank → insufficient evidence |
| `conflict` | the same key maps to different canonical entities |

### Decision outcomes (S290)

`accepted_for_governed_application`, `rejected`, `unresolved`, `conflicting`,
`deferred_for_review`. Only a `matched` candidate is accepted; ambiguous /
unresolved / conflict are never coerced into a match.

## Canonical safety (S279 / S280 / S288 / S297)

- Similarity or confidence never establishes Canonical Identity.
- A candidate is NOT a Governed Canonical Identity; application requires a
  separate, explicit governed step (out of scope here).
- Ambiguous / unresolved / conflict are first-class outcomes.
- Source identity, provenance, evidence, and confidence are preserved and
  attributable (S289).
- Decisions are append-only and replayable (S290 / S297); history is never
  silently rewritten.
- Resolution creates no canonical entity and never mutates Canonical Truth
  (`canonical_mutation` is always `False`).

## Fail-closed behavior

The runtime MUST reject:

- a policy with blank id/version, no signals, or duplicate signals;
- a record with blank source system / identity / canonical ref / provenance;
- an `IdentityDecision` with `canonical_mutation = True`;
- an invalid outcome / confidence on a candidate or decision;
- identity resolution over an unmapped (non-`MAPPED`) canonicalization result.

## Deterministic reference path

`run_reference_identity_path()` uses an ERP `Product` and a WMS `Sku` that share
an explicit GTIN (`08500000001015`) and align on the same canonical entity →
`matched` (→ `accepted_for_governed_application`); a TMS shipment with a unique
GTIN stays `not_matched`. The run is deterministic (identical JSON across runs).

## Non-goals

P7-C does not:

- mutate Canonical Truth, the Canonical Graph, or the Canonical Ontology;
- create a new canonical entity, attribute, or predicate;
- perform fuzzy / probabilistic / ML entity matching;
- apply an accepted match to Canonical Identity (that is a separate governed
  application step, future work);
- add vendor connectors, graph transactions, or third-party dependencies.
