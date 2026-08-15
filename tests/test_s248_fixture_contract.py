from pathlib import Path


def test_s248_fixture_contract_defines_required_fields() -> None:
    text = Path("docs/graph-fixtures/README.md").read_text(encoding="utf-8")
    for field in (
        "canonical entities",
        "canonical relations",
        "source/provenance metadata",
        "deterministic identifiers",
        "expected query results",
        "expected evidence/explanation coverage",
    ):
        assert field in text


def test_s248_defines_initial_fixture_families() -> None:
    text = Path("docs/graph-fixtures/README.md").read_text(encoding="utf-8")
    for family in (
        "supply dependency chain",
        "inventory/capacity chain",
        "multi-hop supply-risk chain",
    ):
        assert family in text
