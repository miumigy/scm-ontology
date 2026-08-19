from pathlib import Path


DOC = Path("docs/history/phase7/S259-m7-provenance-integration.md")


def test_s259_defines_provenance_boundary() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Provenance Record" in text
    assert "Canonicalization Result" in text


def test_s259_requires_source_lineage() -> None:
    text = DOC.read_text(encoding="utf-8")
    for field in ("source_system", "source_record_id", "source_field_or_relation", "mapping_rule_id", "mapping_decision_id"):
        assert f"`{field}`" in text


def test_s259_separates_provenance_from_truth() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "Provenance is not truth" in text
    assert "MUST NOT silently promote Evidence into a Canonical Fact" in text


def test_s259_preserves_transformation_lineage() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "original representation reference" in text
    assert "transformation context" in text


def test_s259_retains_gap_provenance() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "ambiguous" in text
    assert "unmappable" in text
    assert "rejected" in text
    assert "MUST NOT be discarded" in text


def test_s259_forbids_canonical_mutation() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT create a new canonical entity, attribute, or predicate" in text
    assert "MUST NOT mutate canonical facts" in text
    assert "MUST NOT infer a canonical fact from provenance alone" in text
