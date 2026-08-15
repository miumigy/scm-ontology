# M4 Architecture Freeze

## Purpose

M4 freezes the semantic and runtime boundaries established through S229 before advanced reasoning features are added.

## Layer model

```text
Canonical Semantic Model
        |
        +-- Canonical Graph
        |
        +-- Query / Traversal
        |
        +-- Constraint Evaluation
        |
        +-- Evidence / Provenance
        |
        +-- Reasoning Result
        |
        +-- Explanation / Confidence
        |
        +-- Reasoning Policy
        |
        +-- External Adapters
```

## Responsibility boundaries

### Canonical Semantic Model
Defines stable SCM concepts, predicates, identities, and relation semantics. It is independent of enterprise products and AI reasoning.

### Canonical Graph
Stores canonical nodes and relationships. It is the semantic source of truth and is not mutated by default reasoning operations.

### Query / Traversal
Reads canonical graph structure and returns existing paths. It does not infer missing edges.

### Constraint Evaluation
Evaluates explicit constraints against existing paths. It does not repair or infer paths.

### Evidence / Provenance
Associates transport-neutral source references with observations or reasoning paths. Evidence does not redefine canonical identity.

### Reasoning Result
Records the output of deterministic reasoning operations. Results are not automatically promoted to canonical truth.

### Explanation / Confidence
Explanation is a deterministic trace derived from result identities and evidence. Confidence is derived metadata with explicit factors. Neither is canonical truth.

### Reasoning Policy
Controls whether inference, graph mutation, and truth-class promotion are permitted. The safe default is read-only and non-promoting.

### External Adapters
Map ERP/WMS/TMS/planning and other enterprise representations into or out of the canonical model without changing canonical semantics.

## Frozen invariants

1. Canonical truth is distinct from derived and inferred information.
2. Reasoning is read-only by default.
3. Inferred information cannot become canonical truth implicitly.
4. Evidence and confidence are metadata, not semantic truth.
5. Enterprise-specific identifiers do not define canonical identity.
6. Missing graph facts are not silently invented by traversal.
7. Explanation must be derivable from existing result/evidence state.

## M4 exit criterion

Future reasoning features must compose with these boundaries rather than introduce new truth semantics inside the reasoning runtime.
