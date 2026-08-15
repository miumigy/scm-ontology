from pathlib import Path


def test_uc03_contains_flow_contract() -> None:
    text = Path("docs/use-cases/UC-03-material-flow.md").read_text(encoding="utf-8")
    for value in ("moves", "from", "to", "no_match", "Evidence", "Explanation", "Confidence"):
        assert value in text


def test_uc03_preserves_non_inference_boundary() -> None:
    text = Path("docs/use-cases/UC-03-material-flow.md").read_text(encoding="utf-8")
    assert "silently creating missing movements" in text
    assert "without silently creating missing movements" in text
