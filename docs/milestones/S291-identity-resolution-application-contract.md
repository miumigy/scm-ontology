# S291 — Identity Resolution Application Contract

## Purpose

Define the governed application boundary that turns an accepted identity-resolution Decision into an auditable Canonical Identity application without permitting implicit graph mutation.

## Application Preconditions

A Canonical Identity application MUST reference:

- the identity-resolution Decision
- the evidence and provenance supporting that Decision
- the source identities in scope
- the governing policy or authorization context
- the intended Canonical Identity change

An application MUST be rejected or remain pending when the required Decision, evidence, provenance, or governance context is missing.

## Canonical Safety Invariants

- MUST NOT create a new canonical entity, attribute, or predicate automatically outside the governed Application.
- MUST NOT mutate canonical facts implicitly.
- MUST NOT infer Canonical Truth from application success alone.
- Conflicts MUST remain observable.
- Source identity and provenance MUST remain attached.
- Semantic Gap and unresolved identity MUST remain first-class outcomes.
- Reasoning MUST remain read-only.
- An application result MUST be auditable and attributable to its governing Decision.

## Historical Integrity

Application Records MUST be append-only.

A later correction, rejection, rollback request, or re-application MUST create a new governed record and MUST NOT silently rewrite the historical application decision.

Application execution MUST be replayable from its recorded inputs and governance context. Replay MUST produce a distinct result and MUST NOT rewrite historical records.

## Scope Boundary

The Application contract authorizes only the explicitly described Canonical Identity change. It MUST NOT expand scope by creating unrelated entities, attributes, predicates, or facts.

Any conflict, unresolved identity, Semantic Gap, or governance failure MUST remain observable rather than being silently normalized.

## Non-Goals

This contract does not define a graph transaction engine, authorization implementation, UI approval workflow, rollback mechanism, automatic identity merging, production synchronization, or autonomous governance.
