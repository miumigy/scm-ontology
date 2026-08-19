from pathlib import Path

DOC = Path("docs/history/phase8/S302-temporal-historical-query-contract.md")


def test_s302_requires_explicit_temporal_basis() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Every temporal query MUST declare its temporal basis",
        "Effective Time, Recorded Time",
        "A query MUST NOT silently substitute Recorded Time for Effective Time",
        "Open-ended and future-effective facts MUST have explicit temporal semantics",
    ):
        assert phrase in text


def test_s302_preserves_historical_truth() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "A historical query MUST be evaluated against the applicable Fact Version and lifecycle history",
        "The result MUST be reconstructable from retained Fact Versions and append-only lifecycle transitions",
        "Superseded, retired, invalidated, disputed, and deferred states MUST remain distinguishable",
        "A historical query MUST NOT mutate Canonical Facts",
        "A historical query MUST NOT be silently answered with the current Canonical Truth",
    ):
        assert phrase in text


def test_s302_preserves_temporal_conflicts_and_replayability() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Overlapping Fact Versions MUST remain observable",
        "Temporal overlap MUST NOT be resolved by silently discarding one Fact Version",
        "Conflicting historical assertions MUST remain linked to their conflict or resolution records",
        "The same historical query against the same immutable Fact Version and lifecycle history MUST be replayable",
        "Query execution MUST NOT rewrite historical application outcomes or resolution decisions",
    ):
        assert phrase in text


def test_s302_requires_explicit_query_outcomes_and_read_only_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "`resolved`, `unresolved`, `conflicted`, `not-recorded`, or `unsupported-temporal-semantics`",
        "`resolved` MUST reference the applicable Fact Version",
        "`unresolved` MUST remain observable",
        "`conflicted` MUST expose the relevant competing assertions",
        "`not-recorded` MUST indicate that the requested historical state is not present",
        "Temporal Query, Historical Reconstruction, Reporting, Projection, and Replay MUST remain read-only",
        "They MUST NOT create, update, delete, supersede, invalidate, or otherwise mutate Canonical Facts",
    ):
        assert phrase in text
