from pathlib import Path


DOC = Path("docs/history/phase7/S260-m7-semantic-gap-contract.md")


def test_s260_defines_distinct_gap_classes() -> None:
    text = DOC.read_text(encoding="utf-8")
    for gap_class in (
        "ambiguous",
        "unmappable",
        "unsupported",
        "vendor_specific",
        "insufficient_evidence",
        "conflicting_semantics",
    ):
        assert f"`{gap_class}`" in text


def test_s260_preserves_gap_lineage() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "source_representation" in text
    assert "provenance" in text
    assert "mapping_attempt_id" in text


def test_s260_forbids_automatic_ontology_expansion() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT automatically trigger ontology extension" in text
    assert "MUST NOT cause automatic creation, modification, or extension" in text


def test_s260_forbids_canonical_mutation() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MUST NOT create a new canonical entity, attribute, or predicate automatically" in text
    assert "MUST NOT mutate canonical facts" in text
    assert "MUST NOT infer a canonical fact from a gap classification" in text


def test_s260_supports_explicit_non_canonicalized_results() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "A Semantic Gap result is therefore an explicit outcome" in text


def test_s260_separates_governance_from_runtime() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "separate, explicit ontology-governance decision" in text
    assert "MUST NOT mutate the Canonical Ontology as a side effect" in text
