from pathlib import Path

DOC = Path("docs/history/phase8/S305-projection-query-contract.md")


def test_s305_requires_explicit_query_identity_and_semantics() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Every projection query MUST identify the projection definition",
        "temporal basis, scope, and freshness requirements",
        "MUST NOT silently reinterpret missing parameters",
    ):
        assert phrase in text


def test_s305_preserves_canonical_boundary_and_lineage() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Projection query results MUST remain distinguishable from Canonical Truth",
        "A projection query MUST NOT create, update, delete, supersede, invalidate",
        "Query execution MUST NOT alter provenance, evidence, conflict records",
        "A projection result MUST preserve references to its source lineage",
    ):
        assert phrase in text


def test_s305_preserves_freshness_temporal_and_scope_semantics() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "A freshness-constrained query MUST expose whether the projection satisfies",
        "A stale or unknown-freshness projection MUST NOT be silently returned as current Canonical Truth",
        "Historical or point-in-time projection queries MUST preserve",
        "Temporal ambiguity MUST remain observable",
        "Query scope MUST remain explicit and MUST NOT expand implicitly",
    ):
        assert phrase in text


def test_s305_requires_uncertainty_replayability_and_outcomes() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Conflicted, unresolved, stale, unavailable, and unsupported results MUST remain observable",
        "A query MUST NOT silently discard conflicting source states",
        "An unresolved result MUST NOT be promoted to Canonical Truth",
        "Query execution MUST be replayable",
        "`resolved`, `stale`, `unknown-freshness`, `conflicted`, `unresolved`, `not-available`, or `unsupported`",
    ):
        assert phrase in text
