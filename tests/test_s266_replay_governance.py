from pathlib import Path


DOC = Path("docs/history/phase7/S266-m7-replay-governance-contract.md")


def test_s266_defines_governance_signal_traceability() -> None:
    text = DOC.read_text(encoding="utf-8")
    for field in (
        "signal_id",
        "result_id",
        "reason",
        "affected mapping dimensions",
        "provenance references",
        "semantic-gap references",
    ):
        assert f"`{field}`" in text or field in text
    assert "MUST remain traceable to the replay comparison" in text


def test_s266_defines_reviewable_triggers() -> None:
    text = DOC.read_text(encoding="utf-8")
    for trigger in (
        "changed canonical target",
        "changed decision",
        "changed mapping confidence",
        "changed provenance",
        "changed semantic-gap classification",
        "non-reproducible execution",
        "repeated ambiguity or unmappable outcomes",
    ):
        assert trigger in text


def test_s266_separates_review_from_replay() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "The review workflow MUST be distinct from replay execution" in text
    assert "a separate controlled action" in text


def test_s266_preserves_canonical_truth_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT create a new canonical entity, attribute, or predicate automatically" in text
    assert "MUST NOT mutate canonical facts" in text
    assert "MUST NOT infer a canonical fact from a governance signal alone" in text
    assert "MUST NOT rewrite historical audit records" in text
    assert "MUST NOT expand the Canonical Ontology merely because an enterprise representation is unmappable" in text


def test_s266_treats_semantic_gap_as_proposal_not_fact() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST identify the gap rather than inventing a canonical target" in text
    assert "remains a governance proposal until separately accepted" in text


def test_s266_requires_explainability() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Every governance signal MUST expose why it was raised" in text
