# SCM Semantics

This directory is the **normative semantic specification** of SCM Ontology: the
canonical entities, relationships, events, states, constraints, decisions, KPIs,
risks, evidence/provenance, temporal semantics, and reasoning contracts that make
up the current model.

Each file documents one semantic contract. The filename prefix (for example
`S116`) is a **stable historical identifier** used to trace the contract back
through the development record. It is not a planning sequence to be extended;
future semantic development is managed by public release (see the repository
[`README.md`](../../README.md) and [`BACKLOG.yaml`](../../BACKLOG.yaml)).

The semantic model this directory describes is **unchanged** by the v0.1.0
productization: the canonical ontology, relationships, registry, schemas,
and validator specifications are preserved as released.

## Reading entry points

- Start with the canonical core: `canonical entity/relationship/event/state` contracts in this directory.
- Then move to evidence/provenance, temporal, assertion, and reasoning contracts.
- For the current architecture and governed runtime, see [`docs/architecture/`](../architecture/)
  and [`docs/operations/`](../operations/).
- For how to use the released product, start at the repository
  [`README.md`](../../README.md) and [`docs/launch/`](../launch/README.md).
