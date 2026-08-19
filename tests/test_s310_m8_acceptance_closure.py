from pathlib import Path

DOC = Path("docs/history/phase8/S310-m8-acceptance-closure.md")


def test_s310_defines_end_to_end_governed_chain() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Source Evidence → Adapter / Mapping → Canonical Identity → Canonical Fact → Fact Version → Conflict / Resolution → Historical Query → Projection → Materialization → Invalidation → Cross-Projection Consistency → Operational Governance",
        "Every transition MUST preserve applicable identity, provenance, scope, temporal basis, lifecycle state, and lineage.",
    ):
        assert phrase in text


def test_s310_protects_canonical_truth_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "No stage in the M8 lifecycle MUST create a new canonical entity, attribute, or predicate automatically.",
        "Mapping success MUST NOT establish Canonical Truth by itself.",
        "Identity similarity MUST NOT by itself establish Canonical Identity.",
        "Canonical Facts MUST NOT be implicitly mutated",
        "Any Canonical mutation MUST occur through an explicit governed application step.",
    ):
        assert phrase in text


def test_s310_preserves_history_conflicts_and_projection_lineage() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Historical queries MUST NOT silently return current Canonical Truth.",
        "Conflict and Resolution Records MUST remain append-only.",
        "Historical conflict or resolution decisions MUST NOT be silently rewritten.",
        "Resolution execution MUST remain replayable.",
        "Materialization and refresh MUST preserve historical lineage",
        "Rebuild MUST be deterministic and replayable",
    ):
        assert phrase in text


def test_s310_requires_observable_uncertainty_and_consistency_boundaries() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Partial, failed, stale, invalid, conflicted, unresolved, and unsupported projection outcomes MUST remain observable.",
        "Affected projections MUST be distinguishable as stale, invalid, rebuild-required, or unknown-impact",
        "Unknown or partial consistency results MUST NOT be promoted to consistent.",
        "A projection discrepancy MUST NOT by itself establish which result is Canonical Truth.",
        "Conflicting projection results MUST remain observable",
    ):
        assert phrase in text


def test_s310_defines_release_blocking_invariants_and_closeout() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Provenance",
        "Lineage",
        "Observability",
        "No implicit Canonical mutation",
        "Replayability",
        "Scope isolation",
        "Semantic stability",
        "all M8 contract tests pass",
        "S294 through S309 contracts remain present and mutually consistent",
        "no known acceptance criterion is satisfied merely by weakening a boundary",
        "M8 establishes the governed semantic and operational contract",
    ):
        assert phrase in text
