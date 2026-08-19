from pathlib import Path


CONTRACT = Path("docs/history/phase7/S255-m7-canonicalization-boundary-contract.md")


def test_s255_defines_directional_adapter_boundary() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    assert "Enterprise Representation → Canonical Semantics" in text
    assert "Canonicalization record contract" in text
    assert "canonical_mutation" in text


def test_s255_requires_mapping_metadata() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    for term in (
        "enterprise_representation",
        "canonical_target",
        "mapping_status",
        "mapping_confidence",
        "provenance",
        "semantic_gap",
    ):
        assert term in text


def test_s255_has_non_promoting_ambiguous_and_unmappable_states() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    for status in ("`mapped`", "`ambiguous`", "`unmappable`", "`rejected`"):
        assert status in text
    assert "No canonical fact is created from the ambiguous mapping." in text
    assert "records the gap instead of inventing a canonical concept" in text


def test_s255_blocks_vendor_semantic_contamination() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    assert "vendor_specific_semantics" in text
    assert "SAP Material Type = ROH" in text
    assert "does not define a canonical SCM relationship by itself" in text


def test_s255_preserves_provenance_without_equating_it_to_truth() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    assert "Adapter provenance answers **where the mapping came from**." in text
    assert "It does not answer **whether the resulting canonical fact is true**." in text
    assert "mapping confidence as fact confidence" in text
