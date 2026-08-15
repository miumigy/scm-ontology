# S264 — M7 Mapping Replay / Reproducibility Contract

## Purpose

Define when an enterprise canonicalization decision can be replayed and compared with its historical result without mutating Canonical Truth.

## Replay identity

A replay MUST identify the semantic inputs that determine the decision:

- `source_representation`
- `mapping_rule_id`
- `mapping_rule_version`
- `adapter_version`
- relevant `transformation_metadata`
- relevant `provenance`
- `semantic_gap` context when applicable

The replay identity MUST be sufficient to distinguish a historical mapping execution from a later execution using changed rules or adapter logic.

## Replay boundary

```text
Historical Audit Record
        ↓
Replay Identity
        ↓
Same Mapping Inputs / Versions
        ↓
Replay Decision
        ↓
★ Compare with Historical Result
```

Replay is an evaluation of adapter behavior. It MUST NOT be treated as a mechanism for asserting business truth.

## Determinism

For equivalent source representation, mapping rule version, adapter version, transformation inputs, and relevant context, replay SHOULD produce the same semantic decision.

If the replay environment cannot reproduce the historical decision, the discrepancy MUST remain explicit and explainable. It MUST NOT be silently normalized to the historical result.

## Version isolation

A replay using a newer adapter or mapping-rule version is a new execution. It MUST NOT overwrite the historical audit record or historical Canonicalization Result.

Historical results MUST remain associated with the versions that produced them.

## Comparison

Replay comparison SHOULD distinguish at least:

- same decision
- changed decision
- changed canonical target
- changed mapping confidence
- changed provenance or semantic-gap classification
- non-reproducible execution

A changed decision is a signal for adapter or mapping-rule review, not permission to mutate Canonical Truth automatically.

## Reproducibility evidence

A replay result SHOULD preserve enough metadata to explain:

- which source representation was replayed;
- which mapping rule and version were used;
- which adapter version was used;
- which relevant transformations were applied;
- why the replay decision was produced.

Replay metadata MUST NOT collapse these dimensions into an opaque status.

## Canonical Truth boundary

Replay is read-only with respect to the Canonical Ontology and Canonical Facts.

The replay process:

- MUST NOT create a new canonical entity, attribute, or predicate automatically;
- MUST NOT mutate canonical facts;
- MUST NOT infer a canonical fact from replay output alone;
- MUST NOT rewrite historical audit records;
- MUST NOT treat replay agreement as proof that the underlying business fact is true.

## Relationship to auditability

S263 establishes historical audit lineage. S264 establishes the conditions under which that lineage can be replayed and compared.

A replay discrepancy MUST remain traceable to the relevant source representation, mapping rule version, adapter version, transformation context, or other recorded input rather than being hidden as a generic failure.

## Non-goals

S264 does not define execution infrastructure, a database schema, automated remediation, canonical fact ingestion, ontology governance, automatic ontology learning, vendor connectors, or graph mutation.
