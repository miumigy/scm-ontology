# S285 — M8 Canonical Application Record

## Purpose

Define the auditable record produced by an explicit governed application of an approved decision to Canonical Graph state.

The Application Record is an audit artifact. It is not itself an authorization, inference, or source of Canonical Truth.

## Required fields

An Application Record MUST identify:

- a unique application record identifier;
- the Decision Record that explicitly authorized the application;
- the application actor or governing authority;
- the application timestamp;
- the target Canonical entities, attributes, and/or predicates affected;
- the requested operation and bounded scope;
- the pre-application Canonical state reference;
- the resulting Canonical state reference, when application succeeds;
- the relevant source identity and provenance references;
- the relevant evidence references;
- the application outcome;
- validation or precondition results;
- a link to the preceding audit record when an append-only sequence is used.

## Outcome

Application outcomes MUST be explicit. At minimum, the record MUST distinguish:

- Applied
- Rejected
- Failed
- Superseded

A rejected or failed application MUST NOT be represented as an Applied result.

## Audit invariants

1. Every Applied result MUST reference an Approved Decision Record.
2. Application history MUST be append-only.
3. An Application Record MUST NOT silently rewrite a previous Application Record.
4. Source identity, provenance, and evidence MUST remain traceable after application.
5. The record MUST preserve the distinction between the decision that authorized an application and the Canonical state resulting from that application.
6. The Application Record MUST NOT be treated as evidence that independently establishes Canonical Truth.
7. A successful application MUST be attributable to an explicit governed application step.
8. Replay MUST be possible from the recorded decision, scope, pre-state reference, and application metadata.

## Mutation boundary

The Application Record records a governed state transition; it does not cause one merely by existing.

Creating, storing, or replaying an Application Record MUST NOT automatically mutate the Canonical Graph.

Application logic MUST NOT:

- create a new canonical entity, attribute, or predicate implicitly;
- infer Canonical Truth from the Application Record alone;
- discard conflicting source assertions or provenance;
- import vendor-specific semantics into the Canonical Ontology;
- turn an Applied record into a new authorization for unrelated mutations.

## Relationship to reasoning

Reasoning may read Application Records to explain how Canonical state was established. Reasoning MUST remain read-only and MUST NOT create or alter Application Records as a side effect of answering a question.

## Non-goals

S285 does not implement a persistence schema, transaction engine, authorization service, graph database mutation, automatic replay executor, or production synchronization connector.
