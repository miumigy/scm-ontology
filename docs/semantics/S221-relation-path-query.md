# S221 — Relation Path Query

S221 introduces an explicit multi-hop relation-path query over the canonical graph.

```text
Product
  --supplies-->
Supplier
  --located_at-->
Site
```

A `RelationPathQuery` declares one canonical start node and an ordered predicate sequence. A match preserves both traversed node identities and relationship identities.

The query is read-only and exact: it follows only existing canonical relationships with the requested predicates. It does not infer missing edges or mutate graph state.
