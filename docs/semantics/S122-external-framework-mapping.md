# S122 — External Framework Semantic Mapping

## Purpose

S122 defines how external SCM frameworks and qualification/reference systems can be mapped to the SCM Ontology without making any framework the ontology itself.

Representative sources include SCOR and APICS/ASCM CPIM, CSCP, and CLTD. They are reference frameworks, not canonical semantics.

## Boundary

```text
Reference Framework
      ↓
Framework Concept / Practice / Process
      ↓
Semantic Mapping
      ↓
Canonical Concept / Relationship / Pattern
```

A framework term is never canonical merely because it has a familiar name.

## Mapping metadata

A framework mapping should preserve:

- framework name
- framework version or edition when known
- source concept identifier
- source label
- source description
- canonical target
- mapping type
- mapping status
- confidence
- rationale
- provenance

## Mapping types

- exact: source semantics substantially match the canonical concept
- broader: source concept covers multiple canonical concepts
- narrower: source concept specializes a canonical concept
- composite: source concept corresponds to a pattern of canonical concepts
- contextual: source concept adds framework context without changing the canonical concept
- adjacent: related but not equivalent
- unmapped: no defensible canonical correspondence yet

`exact` does not mean the source term and canonical term are synonyms in every context; the mapping remains versioned and provenance-bearing.

## Framework-specific structure

Framework process hierarchies, maturity models, competency structures, and prescribed methods remain source-side structures.

For example:

```text
SCOR process structure
CPIM competency structure
CSCP domain structure
CLTD domain structure
        ↓
Semantic Mapping
        ↓
Canonical SCM concepts
```

The hierarchy itself is not copied into Core unless an independently justified canonical relationship exists.

## Qualification boundaries

CPIM, CSCP, and CLTD are knowledge/reference sources. Their terminology may provide evidence for mapping but must not create qualification-specific entities in Core Ontology.

## Provenance and versioning

Framework mappings must preserve source version/edition and provenance. A revised framework may change its terminology or grouping without changing historical canonical assertions.

## Non-goals

S122 does not reproduce copyrighted framework content, define framework curricula, or claim that one framework is the authoritative definition of SCM.

It also does not force every framework concept into the ontology. `unmapped` is a valid and important outcome.
