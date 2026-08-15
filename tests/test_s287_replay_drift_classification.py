from pathlib import Path

DOC = Path("docs/milestones/S287-m8-replay-drift-classification-contract.md")


def test_s287_defines_drift_classes() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "SOURCE_DRIFT",
        "MAPPING_DRIFT",
        "SEMANTIC_DRIFT",
        "GOVERNANCE_DRIFT",
        "IDENTITY_DRIFT",
        "EVIDENCE_DRIFT",
        "NO_DRIFT",
    ):
        assert phrase in text


def test_s287_preserves_canonical_safety() -> None:
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "MUST NOT create a new canonical entity, attribute, or predicate automatically",
        "MUST NOT mutate canonical facts implicitly",
        "MUST NOT infer Canonical Truth from absence of detected drift alone",
        "MUST NOT silently resolve ambiguous mappings or identity conflicts",
        "MUST NOT rewrite the historical Application Record",
        "Reasoning MUST remain read-only",
    ):
        assert phrase in text


def test_s287_requires_governed_follow_up() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "A detected drift is an observation, not an authorization to mutate Canonical State." in text
    assert "a new governed Decision Record" in text
