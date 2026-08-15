from pathlib import Path


def test_uc06_contains_lead_time_contract() -> None:
    text = Path("docs/use-cases/UC-06-lead-time-dependency.md").read_text(encoding="utf-8")
    for value in ("has_lead_time", "affects", "no_match", "Evidence", "Explanation", "Confidence"):
        assert value in text


def test_uc06_preserves_temporal_non_inference_boundary() -> None:
    text = Path("docs/use-cases/UC-06-lead-time-dependency.md").read_text(encoding="utf-8")
    assert "without inventing missing temporal facts" in text
    assert "without graph mutation" in text
