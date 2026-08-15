# S235 — SCM Reasoning Patterns

S235 introduces reusable SCM reasoning patterns as named path templates.

Patterns are semantic usage templates, not ontology definitions. They reference canonical predicates but do not add new predicates or facts.

Initial patterns:

- `supply_dependency`: `depends_on → supplied_by`
- `site_dependency`: `supplied_by → located_at`
- `flow_dependency`: `moves → from → to`

```text
Canonical Predicates
       ↓
SCM Reasoning Pattern
       ↓
RelationPathQuery
       ↓
Reasoning Runtime
```

Patterns remain transport-neutral and enterprise-system independent.
