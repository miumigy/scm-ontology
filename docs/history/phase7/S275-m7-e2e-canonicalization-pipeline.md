# S275 — M7 End-to-End Canonicalization Pipeline

## Purpose

Define the executable boundary that connects Enterprise Data to the Canonical SCM Graph through the controlled M7 Adapter contracts.

## Pipeline

```text
Enterprise Data
      ↓
Entity Mapping
      ↓
Attribute Mapping
      ↓
Predicate / Relation Mapping
      ↓
Mapping Decision
      ↓
Canonicalization Result
      ↓
Provenance / Audit
      ↓
Canonical Graph
```

The pipeline is an orchestration boundary. It does not create Canonical Semantics or Canonical Truth implicitly.

## Execution contract

An execution MUST:

1. identify the source representation and adapter version;
2. identify the mapping configuration and decision versions;
3. apply only approved mappings;
4. preserve provenance and mapping confidence;
5. preserve explicit ambiguity and Semantic Gap outcomes;
6. produce a deterministic Canonicalization Result for the same versioned input and configuration;
7. make the resulting graph changes traceable to the Canonicalization Result;
8. keep Reasoning read-only with respect to Canonicalization execution.

## Canonical boundary

The pipeline MUST NOT create a new canonical entity, attribute, or predicate automatically.

The pipeline MUST NOT mutate canonical facts without an explicit governed application step.

The pipeline MUST NOT infer Canonical Truth from mapping success alone.

The pipeline MUST NOT silently resolve ambiguous mappings.

The pipeline MUST NOT silently discard unmappable data or provenance.

The pipeline MUST NOT import vendor-specific semantics into the Canonical Ontology.

The pipeline MUST NOT rewrite historical Canonicalization Results.

A mapping failure, ambiguity, or Semantic Gap is an explicit execution outcome and MUST NOT be converted into an ontology change by the pipeline itself.

## Graph application boundary

Canonicalization Result and Canonical Graph mutation are distinct stages. A result MAY be submitted to an explicit governed graph-application step, but execution of the mapping pipeline alone MUST NOT be treated as authorization to mutate Canonical Facts.

Every applied graph change MUST remain traceable to the applicable Canonicalization Result, mapping configuration, source representation, and audit history.

## Replay

The pipeline MUST support replay using the same versioned source representation, Adapter, Mapping Configuration, and Governance Decisions. Replay MUST NOT rewrite the historical execution record.

## Failure behavior

If a required mapping, provenance element, or governance decision is missing, the pipeline SHOULD return an explicit non-success outcome rather than inventing a Canonical value.

## Non-goals

S275 does not define automatic graph mutation, ontology learning, automatic mapping discovery, vendor connectors, or unrestricted production ingestion.
