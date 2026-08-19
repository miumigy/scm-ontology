from pathlib import Path

DOC = Path("docs/history/phase8/S304-projection-freshness-and-lineage-contract.md")


def test_s304_requires_projection_lineage() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Every projection MUST identify the Canonical Fact Versions",
        "Projection lineage MUST remain traceable",
        "A projection MUST NOT be presented as Canonical Truth",
        "Projection lineage MUST be replayable",
    ):
        assert phrase in text


def test_s304_requires_explicit_freshness() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Every projection MUST expose a freshness state",
        "Freshness MUST be evaluated against an explicit source version",
        "A stale projection MUST remain observable as stale",
        "MUST NOT silently treat a stale projection as current Canonical Truth",
        "unknown or unsupported freshness outcome",
    ):
        assert phrase in text


def test_s304_preserves_temporal_scope_and_conflict_semantics() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "A projection MUST preserve the temporal basis",
        "MUST NOT silently mix Effective Time and Recorded Time",
        "Projection scope MUST remain explicit",
        "Conflicting source Fact Versions MUST remain observable",
        "Unresolved, disputed, invalidated, deferred, retired, and superseded source states MUST NOT be silently converted",
    ):
        assert phrase in text


def test_s304_requires_replayability_and_read_only_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "projection generation MUST be deterministic",
        "Projection generation MUST be replayable",
        "Replaying a projection MUST NOT mutate Canonical Facts",
        "Projection refresh MUST NOT rewrite historical projection lineage",
        "Canonical Graph Read, Projection Generation, Projection Refresh, and Projection Replay MUST remain read-only",
        "`current`, `stale`, `unknown-freshness`, `conflicted`, `unresolved`, or `unsupported`",
    ):
        assert phrase in text
