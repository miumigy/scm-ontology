from pathlib import Path


def test_uc01_contains_m5_validation_contract() -> None:
    text = Path("docs/use-cases/UC-01-supply-dependency.md").read_text(encoding="utf-8")
    for field in (
        "Business question",
        "Canonical concepts",
        "Canonical predicates",
        "Path query",
        "Expected result",
        "Evidence",
        "Explanation",
        "Confidence",
        "Semantic gap",
    ):
        assert field in text


def test_uc01_preserves_no_match_and_read_only_boundaries() -> None:
    text = Path("docs/use-cases/UC-01-supply-dependency.md").read_text(encoding="utf-8")
    assert "no_match" in text
    assert "without graph mutation" in text
