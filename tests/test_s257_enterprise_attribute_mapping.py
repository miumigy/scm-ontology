from pathlib import Path


DOC = Path("docs/milestones/S257-m7-enterprise-attribute-mapping.md")


def test_s257_separates_field_from_canonical_attribute() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Enterprise Field" in text
    assert "Canonical Attribute" in text
    assert "Field name is not semantics" in text


def test_s257_preserves_mapping_metadata() -> None:
    text = DOC.read_text(encoding="utf-8")
    for term in (
        "source_field",
        "source_value",
        "mapping_status",
        "mapping_confidence",
        "provenance",
        "transformation",
        "canonical_mutation=false",
    ):
        assert term in text


def test_s257_defines_safe_statuses() -> None:
    text = DOC.read_text(encoding="utf-8")
    for status in ("mapped", "ambiguous", "unmappable", "rejected"):
        assert f"`{status}`" in text


def test_s257_distinguishes_mapping_confidence_from_fact_confidence() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Attribute confidence vs fact confidence" in text
    assert "MUST NOT be interpreted as confidence that the source value itself is true" in text


def test_s257_forbids_automatic_canonical_creation() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT create a new canonical attribute automatically" in text
    assert "MUST NOT mutate canonical facts" in text
