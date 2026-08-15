# S232 — Evidence Aggregation

S232 combines provenance sets from multiple reasoning paths into one transport-neutral `EvidenceSet`.

Aggregation deduplicates identical `source_ref` values while preserving first-seen order.

```text
EvidenceSet A ─┐
EvidenceSet B ─┼→ AggregatedEvidence
EvidenceSet C ─┘
```

Aggregation does not merge or alter canonical facts, infer source agreement, or assign confidence. The resulting source count is descriptive metadata only.
