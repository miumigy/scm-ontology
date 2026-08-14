# S47 — Ontology Linter

## Purpose

S47 defines the first executable semantic validation layer for the SCM Ontology.
The linter validates a relationship against canonical semantic contracts without turning implementation schemas or closed-world vocabulary into ontology requirements.

## Scope

The linter may validate:

- predicate endpoint constraints (S42)
- endpoint cardinality when observed occurrence counts are supplied (S43)
- relationship identity through the canonical `RelationshipInstance` contract (S45)
- relationship version / validity representation when a `RelationshipVersion` is supplied (S46)

Relationship qualifiers remain extensible. Their domain-specific value semantics are not inferred by the linter.

## Unknown predicates

An unknown predicate is **not rejected**. It produces an informational finding:

```text
UNKNOWN_PREDICATE / INFO
```

This preserves the open-world/domain-extension principle. A downstream implementation may choose a stricter policy.

## Validation severity

```text
ERROR   = canonical semantic violation; result is invalid
WARNING = non-fatal semantic concern
INFO    = informational finding; result remains valid
```

S47 does not currently emit warnings. The severity is nevertheless part of the result contract so later rules can be added without changing the result shape.

## Cardinality boundary

Canonical cardinality describes relationship occurrence constraints; it does not contain dataset-level occurrence counts. Therefore cardinality is checked only when `from_count` and/or `to_count` are explicitly supplied by the caller.

The linter must not invent counts from a single relationship instance.

## Validity boundary

S46 defines `valid_from` and `valid_to` as semantic validity fields. S47 checks only the structural requirements already defined by S46. It does not impose timezone, interval arithmetic, overlap, ordering, or persistence rules.

## Canonical result

```text
ValidationResult
├─ valid
└─ issues[]
    ├─ code
    ├─ severity
    └─ message
```

`valid` is false only when at least one issue has severity `ERROR`.

## Explicit non-goals

S47 does not define:

- a database validation schema
- JSON Schema / SHACL / SQL constraints
- persistence or transaction semantics
- automatic repair
- closed-world vocabulary enforcement
- temporal interval algebra
- qualifier value inference
- graph serialization

Those concerns may be addressed by later contracts.
