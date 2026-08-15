from pathlib import Path


def test_uc04_contains_inventory_contract() -> None:
    text = Path("docs/use-cases/UC-04-inventory-dependency.md").read_text(encoding="utf-8")
    for value in ("stocked_at", "serves", "no_match", "Evidence", "Explanation", "Confidence"):
        assert value in text


def test_uc04_preserves_non_inference_boundary() -> None:
    text = Path("docs/use-cases/UC-04-inventory-dependency.md").read_text(encoding="utf-8")
    assert "without inferring inventory that is not represented" in text
    assert "without graph mutation" in text
