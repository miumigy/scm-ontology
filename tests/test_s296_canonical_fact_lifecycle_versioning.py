from pathlib import Path

DOC = Path("docs/history/phase8/S296-canonical-fact-lifecycle-versioning-contract.md")


def test_s296_defines_immutable_versioned_fact_model() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "stable Fact Identity",
        "Fact Version Identity",
        "predecessor and successor relationships",
        "current version",
        "historical version",
        "Historical versions MUST remain immutable",
        "A new state MUST be represented by a new version",
    ):
        assert phrase in text


def test_s296_protects_canonical_truth_and_history() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "MUST NOT mutate an existing historical Fact Version",
        "MUST NOT overwrite historical Canonical Truth in place",
        "MUST NOT infer Canonical Truth merely because a newer source observation exists",
        "A new Canonical Fact Version MUST arise only from an explicit governed Canonical Application",
        "Fact Version history MUST be append-only",
        "MUST NOT silently rewrite historical Fact Versions, lineage, provenance, or lifecycle decisions",
        "Version history MUST be replayable from immutable records",
    ):
        assert phrase in text


def test_s296_preserves_temporal_provenance_and_conflict_semantics() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Observed time",
        "Effective time",
        "Recorded time",
        "These timestamps MUST NOT be conflated",
        "Source identity, provenance, and evidence MUST remain attached to each Fact Version",
        "Conflicting evidence MUST remain observable",
        "Semantic Gap and unresolved identity MUST remain valid outcomes",
        "An Application based on stale expected state MUST be rejected or explicitly re-governed",
        "Conflicting successor attempts MUST remain observable as conflicts",
    ):
        assert phrase in text


def test_s296_requires_attributable_replayable_transitions() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Every version transition MUST be attributable to its governing Application and Decision",
        "before-version",
        "intended successor version",
        "actor or authorization context",
        "transition outcome",
        "Repeated execution of the same governed Application MUST NOT create duplicate Fact Versions",
    ):
        assert phrase in text
