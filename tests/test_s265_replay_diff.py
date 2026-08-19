from pathlib import Path


DOC = Path("docs/history/phase7/S265-m7-replay-diff-contract.md")


def test_s265_defines_required_difference_classes() -> None:
    text = DOC.read_text(encoding="utf-8")
    for classification in (
        "same_decision",
        "changed_decision",
        "changed_canonical_target",
        "changed_mapping_confidence",
        "changed_provenance",
        "changed_semantic_gap",
        "non_reproducible",
    ):
        assert f"`{classification}`" in text


def test_s265_is_version_aware() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "`mapping_rule_version`" in text
    assert "`adapter_version`" in text
    assert "MUST remain attributable to that version change" in text


def test_s265_forbids_silent_normalization() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT be silently normalized to the historical result" in text
    assert "MUST remain explicit and reviewable" in text


def test_s265_separates_governance_signal_from_mutation() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT by itself authorize Canonical Ontology or Canonical Fact mutation" in text


def test_s265_preserves_canonical_truth_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT create a new canonical entity, attribute, or predicate automatically" in text
    assert "MUST NOT mutate canonical facts" in text
    assert "MUST NOT infer a canonical fact from a difference classification alone" in text
    assert "MUST NOT rewrite historical audit records" in text
    assert "MUST NOT interpret `same_decision` as proof" in text


def test_s265_requires_explainability_for_non_reproducible() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "`non_reproducible` MUST include an explainable reason" in text
