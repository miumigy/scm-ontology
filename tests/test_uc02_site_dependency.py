from pathlib import Path


def test_uc02_contains_site_dependency_contract() -> None:
    text = Path("docs/use-cases/UC-02-site-dependency.md").read_text(encoding="utf-8")
    assert "supplied_by" in text
    assert "located_at" in text
    assert "no_match" in text
    assert "without graph mutation" in text


def test_uc02_rejects_vendor_semantics_as_canonical_intent() -> None:
    text = Path("docs/use-cases/UC-02-site-dependency.md").read_text(encoding="utf-8")
    assert "SAP plant code" in text
    assert "WMS warehouse code" in text
    assert "vendor-specific facility identifier" in text
