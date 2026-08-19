from pathlib import Path


DOC = Path("docs/history/phase7/S271-m7-semantic-gap-review-contract.md")


def test_s271_defines_gap_classifications() -> None:
    text = DOC.read_text(encoding="utf-8")
    for value in (
        "ambiguous_mapping",
        "unmappable_representation",
        "missing_evidence",
        "conflicting_evidence",
        "unsupported_scope",
        "canonical_coverage_gap",
    ):
        assert f"`{value}`" in text


def test_s271_requires_traceable_review_record() -> None:
    text = DOC.read_text(encoding="utf-8")
    for field in (
        "gap_id",
        "source representation reference",
        "adapter and mapping versions",
        "gap classification",
        "evidence references",
        "affected scope",
        "review status",
        "resolution decision reference",
        "reviewed_at",
    ):
        assert field in text
    assert "MUST remain traceable" in text


def test_s271_defines_controlled_resolution_options() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "accepting an existing mapping" in text
    assert "requesting additional evidence" in text
    assert "defining a scoped mapping rule" in text
    assert "rejecting the enterprise representation" in text
    assert "proposing a Canonical Ontology change through separate ontology governance" in text
    assert "remains a proposal until separately approved" in text


def test_s271_preserves_canonical_truth_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT create a new canonical entity, attribute, or predicate automatically" in text
    assert "MUST NOT mutate canonical facts" in text
    assert "MUST NOT infer a canonical fact from absence of a gap alone" in text
    assert "MUST NOT rewrite historical audit records" in text
    assert "MUST NOT treat successful mapping as proof" in text
    assert "MUST NOT silently expand an approved mapping" in text


def test_s271_preserves_evidence_distinctions() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Lack of a recorded gap does not mean evidence exists" in text
    assert "absence of evidence MUST remain distinguishable from evidence of absence" in text


def test_s271_requires_controlled_change_and_explainability() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST proceed through a versioned controlled decision" in text
    assert "applicable ontology-governance process" in text
    assert "Existing historical results remain associated with the versions" in text
    assert "what semantic gap was observed" in text
