from pathlib import Path


def test_uc05_contains_capacity_contract() -> None:
    text = Path("docs/use-cases/UC-05-capacity-dependency.md").read_text(encoding="utf-8")
    for value in ("requires_capacity", "provided_by", "no_match", "Evidence", "Explanation", "Confidence"):
        assert value in text


def test_uc05_preserves_non_inference_boundary() -> None:
    text = Path("docs/use-cases/UC-05-capacity-dependency.md").read_text(encoding="utf-8")
    assert "without inferring unrepresented capacity" in text
    assert "without graph mutation" in text
