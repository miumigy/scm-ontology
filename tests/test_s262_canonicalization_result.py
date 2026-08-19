from pathlib import Path


DOC = Path("docs/history/phase7/S262-m7-canonicalization-result-contract.md")


def test_s262_defines_result_record() -> None:
    text = DOC.read_text(encoding="utf-8")
    for field in (
        "result_id",
        "source_representation",
        "canonical_target",
        "decision_state",
        "mapping_confidence",
        "provenance",
        "semantic_gap",
        "reason",
        "transformation_metadata",
    ):
        assert f"`{field}`" in text


def test_s262_preserves_all_decision_states() -> None:
    text = DOC.read_text(encoding="utf-8")
    for state in (
        "mapped",
        "ambiguous",
        "unmappable",
        "unsupported",
        "vendor_specific",
        "insufficient_evidence",
        "conflicting_semantics",
        "rejected",
    ):
        assert f"`{state}`" in text


def test_s262_separates_result_from_canonical_truth() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT be treated as a Canonical Fact automatically" in text
    assert "`canonical_target` identifies a semantic target, not an asserted business fact" in text
    assert "mapping_confidence` is not fact confidence" in text


def test_s262_preserves_provenance_and_gap() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST retain provenance from S259" in text
    assert "Semantic Gap information from S260" in text
    assert "MUST NOT collapse provenance, mapping confidence, and semantic gap" in text


def test_s262_forbids_canonical_mutation() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT create a new canonical entity, attribute, or predicate automatically" in text
    assert "MUST NOT mutate canonical facts" in text
    assert "MUST NOT infer a canonical fact from the result alone" in text


def test_s262_requires_explicit_non_mapped_results() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "A non-mapped result is a valid result" in text
    assert "MUST NOT be converted into an arbitrary target" in text
