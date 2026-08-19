from pathlib import Path


DOC = Path("docs/history/phase7/S258-m7-enterprise-predicate-mapping.md")


def test_s258_preserves_directional_predicate_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Enterprise Relation Representation" in text
    assert "Existing Canonical Predicate" in text
    assert "canonical_mutation=false" in text


def test_s258_requires_provenance_and_mapping_confidence() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "mapping_confidence" in text
    assert "provenance" in text


def test_s258_defines_safe_mapping_statuses() -> None:
    text = DOC.read_text(encoding="utf-8")
    for status in ("mapped", "ambiguous", "unmappable", "rejected"):
        assert f"`{status}`" in text


def test_s258_forbids_automatic_predicate_creation() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT create a new canonical predicate automatically" in text
    assert "MUST NOT mutate canonical facts" in text


def test_s258_preserves_endpoint_integrity() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT silently change the identity or type of either endpoint" in text


def test_s258_does_not_treat_mapping_confidence_as_fact_confidence() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT be interpreted as confidence that the relationship is true" in text
