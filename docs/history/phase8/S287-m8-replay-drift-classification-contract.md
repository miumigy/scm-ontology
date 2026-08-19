# S287 — M8 Replay Drift Classification Contract

## Purpose

Define a controlled classification boundary for differences observed when replaying a governed Canonical Application.

## Drift Classes

Replay differences MUST be classified without silently rewriting the historical Application Record.

Supported classes are:

- `SOURCE_DRIFT` — source representation or source values differ from the recorded inputs.
- `MAPPING_DRIFT` — the applicable mapping definition differs from the recorded mapping context.
- `SEMANTIC_DRIFT` — Canonical semantics or ontology version differs from the recorded context.
- `GOVERNANCE_DRIFT` — decision, policy, authority, or approval conditions differ.
- `IDENTITY_DRIFT` — entity identity resolution differs or becomes unresolved.
- `EVIDENCE_DRIFT` — referenced evidence is unavailable, changed, or no longer supports the same interpretation.
- `NO_DRIFT` — replay context is equivalent for the governed scope.

A replay MAY have multiple drift classes simultaneously.

## Safety Boundary

- MUST NOT create a new canonical entity, attribute, or predicate automatically.
- MUST NOT mutate canonical facts implicitly.
- MUST NOT infer Canonical Truth from absence of detected drift alone.
- MUST NOT silently resolve ambiguous mappings or identity conflicts.
- MUST NOT silently discard unmappable data, evidence, or provenance.
- MUST NOT import vendor-specific semantics into the Canonical Ontology.
- MUST NOT rewrite the historical Application Record.
- Reasoning MUST remain read-only.

## Historical Integrity

The historical Application Record and its original decision context MUST remain immutable and append-only.

A replay observation MUST be stored as a separate result linked to the original Application Record.

Drift classification MUST explain which recorded context differs and MUST preserve the relevant provenance and evidence references.

## Governed Follow-up

A detected drift is an observation, not an authorization to mutate Canonical State.

Any corrective application requires a new governed Decision Record and an explicit application step.

## Non-Goals

This contract does not define automatic drift remediation, autonomous re-application, conflict resolution, ontology version migration, source synchronization, or production transaction execution.
