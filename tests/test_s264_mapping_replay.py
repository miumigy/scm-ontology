from pathlib import Path

DOC = Path("docs/milestones/S264-m7-mapping-replay-contract.md")


def test_s264_defines_replay_identity() -> None:
    text = DOC.read_text(encoding="utf-8")
    for field in ("source_representation", "mapping_rule_id", "mapping_rule_version", "adapter_version", "transformation_metadata", "provenance", "semantic_gap"):
        assert f"`{field}`" in text


def test_s264_requires_version_isolation() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "A replay using a newer adapter or mapping-rule version is a new execution" in text
    assert "MUST NOT overwrite the historical audit record" in text
    assert "Historical results MUST remain associated with the versions that produced them" in text


def test_s264_requires_explicit_discrepancies() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT be silently normalized to the historical result" in text
    assert "same decision" in text
    assert "changed decision" in text
    assert "non-reproducible execution" in text


def test_s264_preserves_reproducibility_explanation() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "which source representation was replayed" in text
    assert "which mapping rule and version were used" in text
    assert "which adapter version was used" in text
    assert "why the replay decision was produced" in text


def test_s264_forbids_canonical_mutation() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT create a new canonical entity, attribute, or predicate automatically" in text
    assert "MUST NOT mutate canonical facts" in text
    assert "MUST NOT infer a canonical fact from replay output alone" in text
    assert "MUST NOT rewrite historical audit records" in text


def test_s264_separates_replay_agreement_from_business_truth() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT treat replay agreement as proof that the underlying business fact is true" in text
