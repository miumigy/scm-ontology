from pathlib import Path

DOC = Path("docs/milestones/S303-canonical-graph-read-projection-boundary.md")


def test_s303_requires_canonical_read_context() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "A Canonical Graph read MUST identify the applicable enterprise scope, temporal basis, and Fact Version context",
        "A read result MUST preserve references to source identity, provenance, evidence, and governing decisions",
        "Historical reads MUST follow the S302 temporal and historical query contract",
        "Conflicts, unresolved identity, disputed facts, and other non-canonical outcomes MUST remain observable",
    ):
        assert phrase in text


def test_s303_separates_projection_from_canonical_truth() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "A projection is a derived read representation and MUST NOT be represented as Canonical Truth",
        "Projection logic MUST be read-only with respect to the Canonical Ontology and Canonical Facts",
        "A projection MUST retain sufficient lineage to identify the Canonical Fact Versions",
        "Derived calculations, aggregations, rankings, classifications, and convenience representations MUST remain distinguishable",
        "A projection MUST NOT silently create, update, delete, supersede, invalidate, or rewrite Canonical Facts",
    ):
        assert phrase in text


def test_s303_preserves_semantics_and_replayability() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "A graph read MUST NOT silently omit provenance, conflicts, unresolved outcomes, or lifecycle state",
        "Transformations that change semantic meaning MUST be explicitly identified as derived or projected semantics",
        "Projection rules MUST NOT introduce vendor-specific semantics into the Canonical Ontology",
        "A projection MUST NOT infer Canonical Truth from aggregation, similarity, ranking, or successful transformation alone",
        "The same projection against the same immutable Canonical Fact Versions and query context MUST be replayable",
        "Stale projections MUST be identifiable and MUST NOT silently masquerade as current Canonical Truth",
    ):
        assert phrase in text


def test_s303_requires_explicit_outcomes_scope_and_read_only_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "`resolved`, `partial`, `conflicted`, `unresolved`, `stale`, `not-found`, or `unsupported`",
        "A projection MUST NOT broaden the scope of the underlying Canonical Graph read implicitly",
        "successful projection execution MUST NOT itself authorize broader access",
        "`conflicted` MUST preserve references to the competing assertions or conflict records",
        "`not-found` MUST NOT be converted into an inferred Canonical entity or fact",
        "Canonical Graph Read, Historical Reconstruction, Projection, Reporting, and Replay MUST remain read-only",
        "They MUST NOT mutate Canonical Facts, Fact Versions, provenance, evidence, conflict records, resolution records, or the Canonical Ontology",
    ):
        assert phrase in text
