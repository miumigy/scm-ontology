# S246 — UC-09 Enterprise Mapping

## Business question

Can enterprise-system representations be mapped to the SCM Ontology without changing or contaminating canonical semantics?

## Canonical intent

Demonstrate a one-way mapping boundary from enterprise representations to canonical concepts and predicates.

## Mapping pattern

```text
SAP / ERP / WMS / TMS / Planning
              ↓
        Adapter Mapping
              ↓
      Canonical Concept
              ↓
      Canonical Predicate
              ↓
       Canonical Graph
```

The adapter translates representations; it does not redefine the meaning of the canonical model.

## M5 validation contract

- Source representation: enterprise-system entity, field, identifier, or relation
- Mapping target: canonical concept and/or predicate
- Mapping rule: explicit and deterministic
- Provenance: source-system and source-record reference retained
- Expected result: canonical representation plus mapping provenance
- Negative case: unmappable or ambiguous source representation must be reported explicitly
- Semantic gap: classify whether the issue belongs to canonical semantics, adapter mapping, or out-of-scope data

## Canonicality test

The following remain source-system representations unless independently justified as canonical semantics:

- SAP material / plant / vendor codes
- ERP document types
- WMS warehouse / bin identifiers
- TMS shipment / carrier identifiers
- APS resource codes
- planning-system object IDs

Adapters must not encode vendor-specific identifiers as canonical ontology predicates.

## Directionality

The mapping boundary is intentionally directional:

```text
Enterprise Representation → Canonical Semantics
```

Canonical semantics must not become dependent on the structure of any single enterprise system.

## Acceptance

The use case passes when representative ERP/WMS/TMS/planning representations can be mapped reproducibly to canonical semantics, with provenance retained and without modifying canonical ontology meaning.
