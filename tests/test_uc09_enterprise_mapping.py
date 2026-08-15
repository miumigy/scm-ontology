from pathlib import Path


def test_uc09_defines_directional_mapping_boundary() -> None:
    text = Path("docs/use-cases/UC-09-enterprise-mapping.md").read_text(encoding="utf-8")
    assert "Enterprise Representation → Canonical Semantics" in text
    assert "Adapter Mapping" in text
    assert "provenance" in text


def test_uc09_rejects_vendor_identifiers_as_canonical_semantics() -> None:
    text = Path("docs/use-cases/UC-09-enterprise-mapping.md").read_text(encoding="utf-8")
    assert "vendor-specific identifiers as canonical ontology predicates" in text
    assert "SAP material / plant / vendor codes" in text
    assert "WMS warehouse / bin identifiers" in text
