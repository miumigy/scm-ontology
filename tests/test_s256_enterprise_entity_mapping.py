from pathlib import Path


DOC = Path("docs/milestones/S256-m7-enterprise-entity-mapping.md")


def test_s256_preserves_directional_entity_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Enterprise Entity Representation" in text
    assert "Canonical Entity Reference" in text
    assert "canonical_mutation=false" in text


def test_s256_requires_provenance_and_mapping_confidence() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "mapping_confidence" in text
    assert "provenance" in text


def test_s256_defines_safe_mapping_statuses() -> None:
    text = DOC.read_text(encoding="utf-8")
    for status in ("mapped", "ambiguous", "unmappable", "rejected"):
        assert f"`{status}`" in text


def test_s256_isolates_vendor_identifiers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "SAP material numbers" in text
    assert "WMS warehouse/bin identifiers" in text
    assert "MUST NOT become canonical ontology predicates" in text


def test_s256_forbids_automatic_ontology_expansion() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT auto-create ontology concepts" in text
