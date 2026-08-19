from pathlib import Path

DOC = Path("docs/history/phase8/S307-projection-invalidation-dependency-contract.md")


def test_s307_requires_dependency_identity_and_invalidation() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Every materialized or queryable projection MUST expose its dependency identity",
        "Dependency tracking MUST remain historical and replayable",
        "MUST produce an explicit invalidation or rebuild-required outcome",
        "`stale`, `invalid`, and `rebuild-required` states MUST remain distinguishable",
        "unknown-impact outcome",
    ):
        assert phrase in text


def test_s307_preserves_impact_scope_and_rebuild_boundaries() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Dependency propagation MUST preserve source identity and provenance",
        "Partial impact MUST remain observable",
        "Cross-projection propagation MUST preserve the dependency chain",
        "Propagation MUST NOT expand across enterprise, tenant",
        "Rebuild MUST NOT mutate Canonical Facts",
        "A rebuild MUST create a distinguishable result",
        "Failed or partial rebuilds MUST remain observable",
    ):
        assert phrase in text


def test_s307_preserves_conflict_resolution_and_history() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "A Canonical conflict, resolution, invalidation, supersession, retirement, or deferral",
        "Conflict resolution MUST NOT silently restore a projection to `current`",
        "Historical projections MUST retain the dependency and resolution context",
        "Replay MUST NOT rewrite historical Canonical or projection records",
    ):
        assert phrase in text


def test_s307_requires_explicit_outcomes_and_read_only_mutation_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "`valid`, `stale`, `invalid`, `rebuild-required`, `unknown-impact`, `partial`, or `failed`",
        "`rebuild-required` MUST NOT be represented as merely stale",
        "`unknown-impact` MUST remain observable",
        "Projection invalidation, dependency propagation, impact analysis, rebuild planning, and replay MUST remain read-only",
        "Any Canonical mutation MUST occur only through an explicit governed application step",
    ):
        assert phrase in text
