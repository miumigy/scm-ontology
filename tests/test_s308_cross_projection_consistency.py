from pathlib import Path

DOC = Path("docs/milestones/S308-cross-projection-consistency-contract.md")


def test_s308_requires_consistency_identity() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Every projection MUST expose its projection definition",
        "Cross-projection comparison MUST compare equivalent definitions",
        "Different projection definitions MUST NOT be treated as inconsistent",
        "Consistency results MUST remain traceable",
    ):
        assert phrase in text


def test_s308_requires_explicit_consistency_outcomes() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "`consistent`, `inconsistent`, `stale`, `invalid`, `rebuild-required`, `unknown`, `partial`, and `failed`",
        "`unknown` MUST NOT be promoted to `consistent`",
        "`partial` MUST identify the incomplete comparison",
        "`failed` MUST remain observable",
    ):
        assert phrase in text


def test_s308_protects_rebuild_and_reconciliation_boundaries() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "A consistency failure MUST produce an explicit governed rebuild",
        "Rebuild planning MUST remain separate from Canonical mutation",
        "Rebuild MUST NOT silently broaden scope",
        "Rebuild MUST create a distinguishable materialization result",
        "Failed, partial, or conflicting rebuilds MUST remain observable",
        "A projection discrepancy MUST NOT by itself establish which projection is Canonical Truth",
        "Conflicting projection results MUST remain observable",
    ):
        assert phrase in text


def test_s308_preserves_temporal_lineage_and_read_only_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Cross-projection consistency MUST respect dependency lineage and Fact Version history",
        "Historical consistency queries MUST evaluate the applicable historical projection versions",
        "Cross-projection comparison, consistency evaluation, reconciliation planning, invalidation analysis, rebuild planning, and replay MUST remain read-only",
        "Any Canonical mutation MUST occur only through an explicit governed application step",
        "Consistency evaluation MUST be replayable",
        "Replaying a consistency evaluation MUST NOT silently rewrite prior outcomes",
    ):
        assert phrase in text
