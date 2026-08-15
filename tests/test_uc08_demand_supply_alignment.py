from pathlib import Path


def test_uc08_contains_alignment_contract() -> None:
    text = Path("docs/use-cases/UC-08-demand-supply-alignment.md").read_text(encoding="utf-8")
    for value in ("demanded_by", "supplied_by", "no_match", "Evidence", "Explanation", "Confidence"):
        assert value in text


def test_uc08_rejects_planning_artifact_promotion() -> None:
    text = Path("docs/use-cases/UC-08-demand-supply-alignment.md").read_text(encoding="utf-8")
    assert "must not silently become a canonical supply fact" in text
    assert "without graph mutation" in text
