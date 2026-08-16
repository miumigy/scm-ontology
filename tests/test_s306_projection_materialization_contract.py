from pathlib import Path

DOC = Path("docs/milestones/S306-governed-projection-materialization-contract.md")


def test_s306_requires_materialization_identity_and_lineage() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Every materialized projection MUST identify its projection definition",
        "Materialization metadata MUST retain source Fact Versions",
        "A materialized projection MUST remain distinguishable from Canonical Truth",
    ):
        assert phrase in text


def test_s306_requires_freshness_and_safe_refresh() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Every materialized projection MUST expose a freshness state",
        "Refresh MUST establish which source state was used",
        "A failed or partial refresh MUST remain observable",
        "Refresh MUST NOT silently change temporal basis, scope, or projection definition",
        "Stale materializations MUST remain explicitly stale",
    ):
        assert phrase in text


def test_s306_preserves_history_and_replayability() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "A new materialization MUST NOT overwrite historical materialization lineage",
        "Historical materialization records MUST remain reconstructable",
        "Materialization refresh MUST NOT rewrite Canonical Facts",
        "Materialization MUST be deterministic",
        "Materialization MUST be replayable",
        "Replay MUST produce a distinguishable materialization result",
    ):
        assert phrase in text


def test_s306_preserves_failure_uncertainty_and_mutation_boundaries() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "`current`, `stale`, `partial`, `failed`, `conflicted`, `unresolved`, and `unsupported`",
        "Partial materialization MUST identify its incomplete state",
        "Conflicted or unresolved source state MUST NOT be silently promoted",
        "An unavailable source state MUST NOT be silently replaced",
        "Materialization, refresh, rebuild, and replay MUST NOT create, update, delete",
        "Any governed Canonical mutation MUST occur through an explicit application step",
    ):
        assert phrase in text
