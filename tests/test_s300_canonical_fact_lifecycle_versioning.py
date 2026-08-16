from pathlib import Path

DOC = Path("docs/milestones/S300-canonical-fact-lifecycle-versioning-contract.md")


def test_s300_defines_explicit_fact_lifecycle() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Every Canonical Fact MUST have an explicit lifecycle state",
        "`proposed`",
        "`active`",
        "`superseded`",
        "`retired`",
        "`invalidated`",
        "`disputed`",
        "A lifecycle transition MUST be explicit, attributable, and governed",
        "A state MUST NOT be inferred merely from the existence of a source observation or a successful mapping",
    ):
        assert phrase in text


def test_s300_preserves_temporal_and_version_semantics() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Every Fact Version MUST distinguish Effective Time from Recorded Time",
        "Temporal information MUST NOT be silently normalized away",
        "Overlapping or contradictory temporal assertions MUST remain observable",
        "Every Canonical Fact Version MUST have a stable, unique version identity",
        "A new version MUST NOT overwrite the historical content of a prior version",
        "Supersession MUST explicitly identify the prior version being superseded",
        "A superseded version MUST remain retrievable as historical state",
    ):
        assert phrase in text


def test_s300_protects_canonical_truth_provenance_and_history() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Current Canonical Truth MUST remain distinguishable from historical Fact Versions",
        "Historical Fact Versions MUST NOT be silently rewritten",
        "Provenance, source identity, evidence, enterprise scope, and governing decision references MUST remain attached",
        "Conflict or dispute MUST NOT be converted into `active` solely for downstream convenience",
        "Fact Version History MUST be append-only",
        "Lifecycle Transition Records MUST be append-only",
        "Historical Fact Versions MUST NOT be silently rewritten or deleted",
        "A correction MUST be represented by a new attributable version or governed lifecycle transition",
    ):
        assert phrase in text


def test_s300_requires_replayable_history_and_observable_invalidation() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Fact lifecycle processing MUST be replayable",
        "Replaying historical events MUST reconstruct the historical state",
        "Replaying current state MUST be distinguishable from reconstructing a historical point in time",
        "Conflicting evidence, disputed assertions, and invalidated facts MUST remain observable and attributable",
        "Invalidation MUST explain the governing reason",
    ):
        assert phrase in text
